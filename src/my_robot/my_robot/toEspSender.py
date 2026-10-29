import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray
import socket
class MySubscriber(Node):
    def __init__(self):
        super().__init__('my_subscriber')
        self.ESP_IP = "192.168.0.60"
        self.ESP_PORT = 4210
        self.cv_active = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sub = self.create_subscription(
            Int32MultiArray, '/motor_pwm', self.joyAction, 10
        )
        self.sub2 = self.create_subscription(
            Int32MultiArray, '/cv_action', self.cvAction, 10
        )
    def joyAction(self, msg):
        if not self.cv_active:
            myString = str(msg.data[0]) + "," + str(msg.data[1]) + "," + str(msg.data[2]) + "," + str(msg.data[3])
            self.sock.sendto(myString.encode('utf-8'),(self.ESP_IP, self.ESP_PORT))
    def cvAction(self, msg):
        if msg.data[0] == -1 and msg.data[1] == -1 and msg.data[2] == -1 and msg.data[3] == -1:
            self.cv_active = False
        else:
            self.cv_active = True
            myString = str(msg.data[0]) + "," + str(msg.data[1]) + "," + str(msg.data[2]) + "," + str(msg.data[3])
            self.sock.sendto(myString.encode('utf-8'),(self.ESP_IP, self.ESP_PORT))
        

def main(args=None):
    rclpy.init(args=args)
    node = MySubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
