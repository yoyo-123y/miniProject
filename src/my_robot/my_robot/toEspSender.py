import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray
import socket
class MySubscriber(Node):
    def __init__(self):
        super().__init__('my_subscriber')
        self.ESP_IP = "192.168.0.60"
        self.ESP_PORT = 4210
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sub = self.create_subscription(
            Int32MultiArray, '/motor_pwm', self.callback, 10
        )

    def callback(self, msg):

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
