import serial
import torch
import time

# Define the AI model (simplified for example)
class ExoNet(torch.nn.Module):
    def __init__(self):
        super(ExoNet, self).__init__()
        self.fc = torch.nn.Linear(3, 2)  # Input: ax, ay, az | Output: angle1, angle2

    def forward(self, x):
        x = self.fc(x)
        return x

# Load the model (assuming it's saved as exonet.pth)
model = ExoNet()
# model.load_state_dict(torch.load('exonet.pth'))
model.eval()

# Set up serial communication
ser = serial.Serial('/dev/ttyUSB0', 115200)

while True:
    try:
        line = ser.readline().decode().strip()
        if line:
            # Parse accelerometer data
            parts = line.split('|')
            ax = float(parts[0].split(':')[1])
            ay = float(parts[1].split(':')[1])
            az = float(parts[2].split(':')[1])

            # Prepare input tensor
            input_tensor = torch.tensor([[ax, ay, az]], dtype=torch.float32)

            # Get model output
            output = model(input_tensor)
            angle1, angle2 = output.detach().numpy()[0]

            # Send control signals back to Arduino
            command = f"{angle1},{angle2}\n"
            ser.write(command.encode())

            print(f"Sent angles: {angle1}, {angle2}")
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(1)

