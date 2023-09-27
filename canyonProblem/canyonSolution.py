import rclpy

from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32 
from builtin_interfaces.msg import Time

class canyonsolution(Node):
	def __init__(self):
		super().__init__("canyonsolution")
		self.pub = self.create_publisher(Twist, "cmd_vel", 10)
		self.timer = self.create_timer(.1, self.move)  # 1 Hz
		
		
		
		self.last_signal_time = self.get_clock().now()
		#left and right sub
		self.left= self.create_subscription(Int32,"left", self.leftcallback,10)
		self.right = self.create_subscription(Int32,"right", self.rightcallback,10)
		self.leftstate = 0
		self.rightstate = 0
		self.state = 0
		self.edgestate=0
		self.last_state_change_time = self.get_clock().now()
		self.left_count = 0
		self.right_count = 0
		self.time_window = 5.0  # 5 seconds

	def leftcallback(self,leftmsg):
		if leftmsg.data == 1:
			self.leftstate = 1
			self.left_count += 1
		elif leftmsg.data == 0:
			self.leftstate = 0
	def rightcallback(self,rightmsg):
		if rightmsg.data == 1:
			self.rightstate = 1
			self.right_count += 1
		elif rightmsg.data == 0:
			self.rightstate = 0
	
	#def edgecounter(self):
	#	msg = Twist()
	#	self.edgestate += 1
	#	if self.edgestate == 5:
	#		msg.angular.z = -10.0
	#		msg.linear.x = -10.0
	#		self.edgestate += 1
			
		
	
	
	#def count_sensor_activations(self, current_time):
        # Calculate the number of sensor activations within the time window
	#	count = 0
	#	if (current_time - self.last_signal_time).nanoseconds / 1e9 <= self.time_window:
	#		count += 1
	#		return count
	
	
	
	def move(self):
		
		msg = Twist()
		current_time = self.get_clock().now()
		
		
		time_diff = (current_time - self.last_state_change_time).nanoseconds / 1e9  # Convert to seconds
		if self.left_count >= 5 or self.right_count >= 5:
		    # If either sensor goes off 5 times or more within the time window
			msg.linear.x = -1.0  # Move backward
			msg.angular.z = 0.0  # Stop turning

		#if self.edgestate == 5:
		#	msg.angular.z = -2.0
		#	msg.linear.x = -10.0
		#	self.edgestate += 1
		
		if self.leftstate == 1 and self.rightstate == 1:
			msg.angular.z = -3.0
			msg.linear.x = -3.0
			
			self.edgestate += 1
		
		#if (self.state != 0 and self.state != 1) and time_diff >= 10.0:
		#	self.state = 1
			
			
		
		
		
		if self.leftstate == 0 and self.rightstate == 0:
			
			
			self.state= 1 
			
		if self.leftstate == 0 and self.rightstate == 1:

			
			self.state= 2
			
		if self.leftstate == 1 and self.rightstate == 0:
			self.state= 3
			
		
		
		
		
		
		
		
		if self.state == 0:
			start_time = time.time()
			msg.linear.x = -1.0
			msg.angular.z = -1.0
			while time.time() - start_time < 1.0:
				msg.angular.z = 1
		if self.state == 1:
			
			# Go forward
			#positive
			msg.linear.x = .7
		if self.state == 2:
			#backup and turn left
			msg.linear.x = -1.0
			msg.angular.z = 2.0
				
			
		if self.state == 3:
			
				#backup and turn right
				msg.linear.x = -1.0
				msg.angular.z = -2.0
				
		current_time = self.get_clock().now()
		time_diff = (current_time - self.last_state_change_time).nanoseconds / 1e9  # Convert to seconds
		if time_diff >= self.time_window:
			self.left_count = 0
			self.right_count = 0
			self.last_state_change_time = current_time
				
				
				
				
		self.pub.publish(msg)
		

def main(args=None):
	rclpy.init(args=args)
	mover = canyonsolution()
	rclpy.spin(mover)
	mover.destroy_node()
	rclpy.shutdown()

if __name__ == '__main__':
	main()


