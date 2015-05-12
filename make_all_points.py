import os

points = list(range(-3, 33))

for point in points:
    if   point  > 0: name = "P" + str(point)
    elif point == 0: name = str(point)
    else           : name = "M" + str(abs(point))

    input_ttcrx  = "data/default/TTCrxPhaseDelayRBX_0x187_tunedHTRs_tuned_v11m.xml"
    input_brick  = "data/default/delay"
    output_ttcrx = "data/shift" + name + "/ttcrx.xml"
    output_brick = "data/shift" + name + "/delay"

    command = "python make_points.py -it " + input_ttcrx + " -ib " + input_brick + " -ot " + output_ttcrx + " -ob " + output_brick + " -s " + str(point)
    
    os.system ( "mkdir -p " + output_brick )
    os.system ( command ) 
    
    
    
