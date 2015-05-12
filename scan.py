import xml.etree.ElementTree as ET
import os
import argparse

class ttcrx:
    def __init__ (self, in_path):
        self.tree = ET.parse ( in_path )
        self.cfg_brick_set = self.tree.getroot()
        self.cfg_brick = self.cfg_brick_set[0]

    def shift_rbx (self, rbx_name, shift ):
        for datum in self.cfg_brick.findall("Data"):
            if datum.attrib["id"] != rbx_name : continue
            old_text = datum.text
            old_value = old_text.split()[0]
            new_value = str(int(old_value) + shift)
            new_text = old_text.replace ( old_value, new_value )
            datum.text = new_text
            break

    def get_rbx_setting ( self, rbx_name ) :
        for datum in self.cfg_brick.findall("Data"):
            if datum.attrib["id"] != rbx_name : continue
            return int( datum.text.split()[0] )

            
    def dump ( self, out_path ) :
        self.tree.write ( out_path )

class brick :
    def __init__(self, in_path ):
        self.HF_CalibRM_number = 4
        self.HBHEHO_CalibRM_number = 5
        self.RBX = "NULL"
        self.in_path = in_path
        self.tree = ET.parse ( in_path )
        self.cfg_brick = self.tree.getroot()
        for p in self.cfg_brick.findall("Parameter"):
            if p.attrib["name"] == "RBX":
                self.RBX = p.text
                break

    def shift_all (self, shift):
        for datum in self.cfg_brick.findall("Data"):
            rm = int(datum.attrib["rm"])
            if rm == self.HF_CalibRM_number     and "HF"     in self.RBX: continue
            if rm == self.HBHEHO_CalibRM_number and "HF" not in self.RBX: continue
            old_value = int(datum.text)
            new_value = old_value + shift
            datum.text = str(new_value)

    def get_min_max(self):
        retval = [999, -999]
        for datum in self.cfg_brick.findall("Data"):
            value = int(datum.text)
            rm = int(datum.attrib["rm"])
            if rm == self.HF_CalibRM_number     and "HF"     in self.RBX: continue
            if rm == self.HBHEHO_CalibRM_number and "HF" not in self.RBX: continue
            if value < retval[0]: retval[0] = value
            if value > retval[1]: retval[1] = value
        return retval[0], retval[1]
    
    def dump(self, out_path):
        self.tree.write ( out_path ) 

class bricks:
    def __init__ (self, in_dir):
        self.brick_in_paths = [ in_dir + "/" + p for p in os.listdir(in_dir) if os.path.isfile(os.path.join(in_dir,p)) and ".xml" in p ]
        self.bricks = [ brick ( p ) for p in self.brick_in_paths ]

    def get_rbx ( self, rbx_name ):
        for brick in self.bricks:
            if brick.RBX == rbx_name:
                return brick
        return 0

    def shift_all ( self, shift ):
        for brick in self.bricks:
            brick.shift_all ( shift )

    def dump(self, out_dir):
        for brick in self.bricks:
            brick.dump ( out_dir + "/" + os.path.basename ( brick.in_path ) )
        
        
class settings:    
    def __init__ (self, in_ttcrx_path , in_brick_path, out_ttcrx_path , out_brick_path, shift ):
        self.in_brick_path  = in_brick_path
        self.in_ttcrx_path  = in_ttcrx_path
        self.out_brick_path = out_brick_path
        self.out_ttcrx_path = out_ttcrx_path
        self.ttcrx  = ttcrx  ( self.in_ttcrx_path )
        self.bricks = bricks ( self.in_brick_path )
        self.shift_value = int(shift)
        self.log_file_name = "log.txt"

        self.brick_min_delay = 0
        self.brick_max_delay = 24
        self.ttcrx_min_delay = 0
        self.ttcrx_max_delay = 225

        self.ttcrx_step_value = 15
        self.ttcrx_step_time_ns = 1.56
        
    def dump_ttcrx ( self ):
        self.ttcrx.dump ( self.out_ttcrx_path )
        
    def dump_brick ( self ) :
        self.bricks.dump ( self.out_brick_path )

    def dump (self):
        self.dump_ttcrx()
        self.dump_brick()

    def shift ( self ):

        log_file = open ( self.log_file_name, "w" ) 

        # Loop through the bricks, as defined by delay files
        for brick in self.bricks.bricks:

            rbx_number = int(brick.RBX[-2:])
            this_brick_min_delay, this_brick_max_delay = brick.get_min_max()

            # Still within brick bounds: no TTCrx playing needed
            if ( this_brick_min_delay + self.shift_value >= self.brick_min_delay and
                 this_brick_max_delay + self.shift_value <= self.brick_max_delay     ):
                
                print brick.RBX, "inside of bounds (don't touch TTCrx):"
                print "\t --> old brick delay bounds = [\t", this_brick_min_delay, "\t,\t", this_brick_max_delay, "\t]"
                print "\t --> old ttcrx delay        =  \t", self.ttcrx.get_rbx_setting ( brick.RBX ) 

                brick.shift_all ( self.shift_value ) 

                this_brick_min_delay, this_brick_max_delay = brick.get_min_max()
                print "\t --> new brick delay bounds = [\t", this_brick_min_delay, "\t,\t", this_brick_max_delay, "\t]"
                print "\t --> new ttcrx delay        =  \t", self.ttcrx.get_rbx_setting ( brick.RBX ), "\n"

            # Outside of bounds: need to play with TTCrx
            else:
                print brick.RBX, "outside of bounds (adjust TTCrx):"
                print "\t --> old brick delay bounds = [\t", this_brick_min_delay, "\t,\t", this_brick_max_delay, "\t]"
                print "\t --> old ttcrx delay        =  \t", self.ttcrx.get_rbx_setting ( brick.RBX )

                delay_for_bricks_ns = 0
                if self.shift_value > 0: delay_for_bricks_ns = self.brick_max_delay - this_brick_max_delay
                else             : delay_for_bricks_ns = self.brick_min_delay - this_brick_min_delay

                delay_for_ttcrx_ns  = self.shift_value - delay_for_bricks_ns
                delay_for_ttcrx_nk  = int(round(float(delay_for_ttcrx_ns) / self.ttcrx_step_time_ns) - .5) + (float(delay_for_ttcrx_ns) / self.ttcrx_step_time_ns > 0)
                delay_for_ttcrx_k   = delay_for_ttcrx_nk * self.ttcrx_step_value

                if ( delay_for_ttcrx_k + self.ttcrx.get_rbx_setting ( brick.RBX ) > self.ttcrx_max_delay or
                     delay_for_ttcrx_k + self.ttcrx.get_rbx_setting ( brick.RBX ) < self.ttcrx_min_delay ):

                    log_file.write ( "Illegal TTCrx delay requested for " + brick.RBX + "\n")
                    log_file.write ("\t --> old brick delay bounds = [\t" + str(this_brick_min_delay) + "\t,\t" + str(this_brick_max_delay)+ "\t]\n")
                    log_file.write ("\t --> old ttcrx delay        =  \t" + str(self.ttcrx.get_rbx_setting ( brick.RBX ) ) + "\n")
                    log_file.write ("\t --> requested shift        = " + str(self.shift_value) + "\n")
                    continue
                     
                
                brick.shift_all     ( delay_for_bricks_ns )
                self.ttcrx.shift_rbx( brick.RBX,  delay_for_ttcrx_k )
                this_brick_min_delay, this_brick_max_delay = brick.get_min_max()
                print "\t --> new brick delay bounds = [\t", this_brick_min_delay, "\t,\t", this_brick_max_delay, "\t]"
                print "\t --> new ttcrx delay        =  \t", self.ttcrx.get_rbx_setting ( brick.RBX ), "\n"
        
class scan_arg_parser:
    def __init__ (self, this_description):
        self.parser = argparse.ArgumentParser(description=this_description)
        self.parser.add_argument ("-it", metavar="IN_TTCRX_FILE" , dest="in_ttcrx_file" , action="store", required=True, help="In  TTCrx file path" )
        self.parser.add_argument ("-ot", metavar="OUT_TTCRX_FILE", dest="out_ttcrx_file", action="store", required=True, help="Out TTCrx file path")
        self.parser.add_argument ("-ib", metavar="IN_BRICK_DIR"  , dest="in_brick_dir"  , action="store", required=True, help="In  brick dir path"  )
        self.parser.add_argument ("-ob", metavar="OUT_BRICK_DIR" , dest="out_brick_dir" , action="store", required=True, help="Out brick dir path" )
        self.parser.add_argument ("-s" , metavar="SHIFT"         , dest="shift"         , action="store", required=True, help="Requested shift in ns")
        
        self.args = self.parser.parse_args()
