from uwsgi import ready

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from std_msgs.msg import Int32MultiArray
import socket
import select
class MySubscriber(Node):
    def __init__(self):
        super().__init__('my_subscriber')
        self.speed = 0;
        self.previousButton=0;
        self.left = 0;
        self.right = 0;
        self.forward = 0;
        self.backward = 0;
        self.speeds = [100, 150, 255];
        self.Recieve_PORT = 4220;
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", 4220))
        self.publisher = self.create_publisher(Int32MultiArray,'/motor_pwm',10)
    def callback(self, msg):
        pwm = Int32MultiArray()
        pwm.data = [0, 0,0,0]
        ready, _, _ = select.select([self.sock], [], [], 0)
        if ready:
            data, addr = self.sock.recvfrom(1024)
            data = data.decode()
            data = data.split(",")
            # forward, backward, left, right, speed
            pwm.data = [int(data[0]), int(data[1]), int(data[2]), int(data[3]), int(data[4])]
            self.forward = int(data[0])
            self.backward = int(data[1])
            self.left = int(data[2])
            self.right = int(data[3])
            self.speed = int(data[4])
            # up-right, up-left, down-right, down-left
            if(self.left == 0 and self.right == 0 and self.forward == 0 and self.backward == 0):
                pwm.data = [0, 0, 0, 0]
            elif(self.left == 1 and self.right == 0 and self.forward == 0 and self.backward == 0):
                pwm.data = [-self.speeds[self.speed], self.speeds[self.speed],-self.speeds[self.speed], self.speeds[self.speed]]
            elif(self.left == 0 and self.right == 1 and self.forward == 0 and self.backward == 0):
                pwm.data = [self.speeds[self.speed], -self.speeds[self.speed],self.speeds[self.speed], -self.speeds[self.speed]]
            elif(self.left == 0 and self.right == 0 and self.forward == 1 and self.backward == 0):
                pwm.data = [self.speeds[self.speed], self.speeds[self.speed],self.speeds[self.speed], self.speeds[self.speed]]
            elif(self.left == 0 and self.right == 0 and self.forward == 0 and self.backward == 1):
                pwm.data = [-self.speeds[self.speed], -self.speeds[self.speed],-self.speeds[self.speed], -self.speeds[self.speed]]
            elif(self.left == 1 and self.right == 0 and self.forward == 1 and self.backward == 0):
                pwm.data = [0, self.speeds[self.speed],0, self.speeds[self.speed]]
            elif(self.left == 0 and self.right == 1 and self.forward == 1 and self.backward == 0):
                pwm.data = [self.speeds[self.speed], 0,self.speeds[self.speed], 0]
            elif(self.left == 1 and self.right == 0 and self.forward == 0 and self.backward == 1):
                pwm.data = [-self.speeds[self.speed], 0,-self.speeds[self.speed], 0]
            elif(self.left == 0 and self.right == 1 and self.forward == 0 and self.backward == 1):
                pwm.data = [0, -self.speeds[self.speed],0, -self.speeds[self.speed]]
            if(pwm.data[0] == -1 and pwm.data[1] == -1 and pwm.data[2] == -1 and pwm.data[3] == -1):
                pwm.data = [-2, -2, -2, -2]
        else:
            pwm.data = [-1, -1, -1, -1]
        self.publisher.publish(pwm)
                

def main(args=None):
    rclpy.init(args=args)
    node = MySubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
