class DataLogger:
    def __init__(self, output_path=None):
        self.output = open(output_path, 'a') if output_path else None
        
    def write(self, message):
        print(message)
        if self.output:
            self.output.write(message + '\n')
            self.output.flush()
            
    def __del__(self):
        if self.output:
            self.output.close()