class DataLogger:
    def __init__(self, output_path=None, hex_mode=False):
        self.hex_mode = hex_mode
        self.output = open(output_path, 'a') if output_path else None
    
    def write(self, message, raw_data=None):
        print(message)
        
        if self.output:
            self.output.write(f"{message}\n")
            if raw_data is not None:
                self._write_raw_data(raw_data)
    
    def _write_raw_data(self, data: bytes):
        if self.hex_mode:
            hex_str = data.hex()
            self.output.write(f"HEX [{len(data)}]: {hex_str}\n")
        else:
            self.output.write(f"RAW [{len(data)}]: {data}\n")
            
    def __del__(self):
        if self.output:
            self.output.close()