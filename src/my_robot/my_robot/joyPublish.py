import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from std_msgs.msg import Int32MultiArray
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
        self.sub = self.create_subscription(
            Joy, 'joy', self.callback, 10
        )
        self.publisher = self.create_publisher(Int32MultiArray,'/motor_pwm',10)
    def callback(self, msg):
        pwm = Int32MultiArray()
        pwm.data = [0, 0]
        if(msg.buttons[10] == 1 and self.previousButton == 0):
            if(self.speed + 1> 2):
                self.speed = 0;
                self.get_logger().info(f'Speed is now {self.speed}')
            else:
                self.speed = self.speed + 1;
                self.get_logger().info(f'Speed is now {self.speed}')
        self.previousButton = msg.buttons[10]
        if(msg.axes[0] > 0.5):
            self.left = 1;
        else:
            self.left = 0;
        if(msg.axes[0] < -0.5):
            self.right = 1;
        else:
            self.right = 0;
        if(msg.axes[1] > 0.5):
            self.forward = 1;
        else:
            self.forward = 0;
        if(msg.axes[1] < -0.5):
            self.backward = 1;
        else:
            self.backward = 0;
        if(self.left == 0 and self.right == 0 and self.forward == 0 and self.backward == 0):
            pwm.data = [0, 0];
        elif(self.left == 1 and self.right == 0 and self.forward == 0 and self.backward == 0):
            pwm.data = [-self.speeds[self.speed], self.speeds[self.speed]];
        elif(self.left == 0 and self.right == 1 and self.forward == 0 and self.backward == 0):
            pwm.data = [self.speeds[self.speed], -self.speeds[self.speed]];
        elif(self.left == 0 and self.right == 0 and self.forward == 1 and self.backward == 0):
            pwm.data = [self.speeds[self.speed], self.speeds[self.speed]];
        elif(self.left == 0 and self.right == 0 and self.forward == 0 and self.backward == 1):
            pwm.data = [-self.speeds[self.speed], -self.speeds[self.speed]];
        elif(self.left == 1 and self.right == 0 and self.forward == 1 and self.backward == 0):
            pwm.data = [0, self.speeds[self.speed]];
        elif(self.left == 0 and self.right == 1 and self.forward == 1 and self.backward == 0):
            pwm.data = [self.speeds[self.speed], 0];
        elif(self.left == 1 and self.right == 0 and self.forward == 0 and self.backward == 1):
            pwm.data = [-self.speeds[self.speed], 0];
        elif(self.left == 0 and self.right == 1 and self.forward == 0 and self.backward == 1):
            pwm.data = [0, -self.speeds[self.speed]];
        self.publisher.publish(pwm)
        self.get_logger().info(f'Received: {self.left} {self.right} {self.forward} {self.backward} {self.speed}')

def main(args=None):
    rclpy.init(args=args)
    node = MySubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
