import socket

eligible_candidates = []  

def check_eligibility(student_data):
    try:
        
        name, reg_no, _, _, cgpa_str, attendance_percentage_str = student_data.split(',')
        cgpa = float(cgpa_str)
        attendance_percentage = float(attendance_percentage_str)
        min_cgpa = 7.5s
        min_attendance_percentage = 80

        if cgpa >= min_cgpa and attendance_percentage >= min_attendance_percentage:
            eligible_candidates.append(f"Reg No: {reg_no}, Name: {name}")
            return f"Reg No: {reg_no}, Name: {name}, Eligible"
        else:
            return f"Reg No: {reg_no}, Name: {name}, Not Eligible"
    except ValueError:
        return " "

def send_eligible_candidates(client_socket, client_address):
    eligible_candidates_message = "\n".join(eligible_candidates)
    client_socket.sendto(eligible_candidates_message.encode(), client_address)

def main():
    server_ip = '127.0.0.1'
    server_port = 12346  

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((server_ip, server_port))

    print("Placement Cell is waiting for data...")

    while True:
        data, client_address = server_socket.recvfrom(1024)
        student_data = data.decode()

        response = check_eligibility(student_data)
        server_socket.sendto(response.encode(), client_address)

if __name__ == "__main__":
    main()
