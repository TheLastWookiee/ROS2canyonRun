import rclpy

from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32 
#from builtin_interfaces.msg import Time

class canyonsolution(Node):
	def __init__(self):
		super().__init__("canyonsolution")
		self.pub = self.create_publisher(Twist, "cmd_vel", 10)
		self.timer = self.create_timer(.25, self.move)  # 1 Hz
		
		#self.last_signal_time = self.get_clock().now()
		#left and right sub
		self.left= self.create_subscription(Int32,"left", self.leftcallback,10)
		self.right = self.create_subscription(Int32,"right", self.rightcallback,10)
		self.leftstate = 0
		self.rightstate = 0
		self.state = 9
		self.edgestate=0
		self.start_time = None
		self.desired_duration=2.0

	def leftcallback(self,leftmsg):
		if leftmsg.data == 1:
			self.leftstate = 1
		elif leftmsg.data == 0:
			self.leftstate = 0
	def rightcallback(self,rightmsg):
		if rightmsg.data == 1:
			self.rightstate = 1
		elif rightmsg.data == 0:
			self.rightstate = 0
	
	def edgecounter(self):
		self.edgestate += 1
	
	
	
	
	
	
	
	def move(self):
		
		msg = Twist()
		current_time = self.get_clock().now()
		if self.state == 0:
			msg.linear.x = -1.5
			msg.angular.z = -3.0
			
		if self.leftstate == 1 and self.rightstate == 1:
			self.state = 0
			msg.angular.z = -1.5
			self.edgecounter()
			
			
		if self.leftstate == 0 and self.rightstate == 0:
			
			
			self.state= 1 
			
		if self.leftstate == 0 and self.rightstate == 1:

			
			self.state= 2
			
		if self.leftstate == 1 and self.rightstate == 0:
			self.state= 3
			
		
		
		if self.edgestate == 5:
			msg.angular.z = 1.0
		
		if self.state ==0:
			msg.linear.x = -1.0
		
		if self.state == 1:
			
				# Go forward
				msg.linear.x = 2.0
		if self.state == 2:
			#backup and turn left
			msg.linear.x = -0.8
			msg.angular.z = 1.0
				
			
		if self.state == 3:
			
				#backup and turn right
				msg.linear.x = -0.8
				msg.angular.z = -1.0
		self.pub.publish(msg)
		

def main(args=None):
	rclpy.init(args=args)
	mover = canyonsolution()
	rclpy.spin(mover)
	mover.destroy_node()
	rclpy.shutdown()

if __name__ == '__main__':
	main()

