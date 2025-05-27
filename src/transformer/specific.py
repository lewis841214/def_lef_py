class SignLineClearer:
    def __init__(self, sign_list):
        self.sign_list = sign_list
        self.end_sign = ';'

    def clear_line(self, line):
        # Strip whitespace from the line
        cleaned_line = line.strip()
        
        # Remove the end sign if present
        if cleaned_line.endswith(self.end_sign):
            cleaned_line = cleaned_line[:-1].strip()
        
        # Remove signs from the beginning of the line
        for sign in self.sign_list:
            if cleaned_line.startswith(sign):
                cleaned_line = cleaned_line[len(sign):].strip()
                break  # Only remove the first matching sign
        
        return cleaned_line
