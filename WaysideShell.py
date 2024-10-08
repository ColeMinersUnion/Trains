import importlib

#input from UI
file_name = ""

def upload_plc():
   
    #file_name = "BluePLC"
    try:
        plc = importlib.import_module(file_name)
        # Now you can use the imported module

    except ImportError:
        print(f"Error: Module '{file_name}' not found.")


    blue_plc = getattr(plc, file_name)         
    return blue_plc


def main():
    print("hi")
    plc = upload_plc()
    plc.say_hi()
    




if __name__ == "__main__":
    main()
