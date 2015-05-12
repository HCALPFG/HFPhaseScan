from scan import *

if __name__ == "__main__":

    parser = scan_arg_parser('Tool for making delay settings')
    
    my_settings = settings (parser.args.in_ttcrx_file , parser.args.in_brick_dir ,
                            parser.args.out_ttcrx_file, parser.args.out_brick_dir,
                            parser.args.shift ) 

    my_settings.shift()
    my_settings.dump()
    

