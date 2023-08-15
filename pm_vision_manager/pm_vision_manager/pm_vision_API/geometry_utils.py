import copy

class Circle:
    def __init__(self, ax1, ax2, radius, ax1_suffix, ax2_suffix, unit):
        self.ax1 = ax1
        self.ax2 = ax2
        self.radius = radius
        self.ax1_suffix = ax1_suffix
        self.ax2_suffix = ax2_suffix
        self.unit = unit

    def change_unit_to(self,new_unit):
        if self.unit == "um" and new_unit == 'mm':
            self.ax1 = self.ax1 * 0.001
            self.ax2 = self.ax2 * 0.001
            self.radius = self.radius * 0.001
            self.unit = new_unit
        elif self.unit == "um" and new_unit == 'm':
            self.ax1 = self.ax1 * 0.001 * 0.001
            self.ax2 = self.ax2 * 0.001 * 0.001
            self.radius = self.radius * 0.001 * 0.001
            self.unit = new_unit
        elif self.unit == "mm" and new_unit == 'um':
            self.ax1 = self.ax1 * 1000
            self.ax2 = self.ax2 * 1000
            self.radius = self.radius * 1000
            self.unit = new_unit
        elif self.unit == "mm" and new_unit == 'm':
            self.ax1 = self.ax1 * 0.001
            self.ax2 = self.ax2 * 0.001
            self.radius = self.radius * 0.001
            self.unit = new_unit
        elif self.unit == "m" and new_unit == 'um':
            self.ax1 = self.ax1 * 1000 * 1000
            self.ax2 = self.ax2 * 1000 *1000
            self.radius = self.radius * 1000 *1000
            self.unit = new_unit
        elif self.unit == "m" and new_unit == 'mm':
            self.ax1 = self.ax1 * 1000
            self.ax2 = self.ax2 * 1000
            self.radius = self.radius * 1000
            self.unit = new_unit
        elif self.unit == "um" and new_unit == 'um':
            pass
        else:
            print("Invalid unit given!")

    def print_circle_information(self):   
        print("Circle Information:")  
        print(f"{self.ax1_suffix}-Koordinate: {self.ax1}")
        print(f"{self.ax2_suffix}-Koordinate: {self.ax2}")
        print(f"Radius: {self.radius}")
        print(f"Unit: {self.unit}")

class Point:
    def __init__(self, ax1, ax2, ax1_suffix, ax2_suffix, unit):
        self.ax1 = ax1
        self.ax2 = ax2
        self.ax1_suffix = ax1_suffix
        self.ax2_suffix = ax2_suffix
        self.unit = unit

    def change_unit_to(self,new_unit):
        if self.unit == "um" and new_unit == 'mm':
            self.ax1 = self.ax1 * 0.001
            self.ax2 = self.ax2 * 0.001
            self.unit = new_unit
        elif self.unit == "um" and new_unit == 'm':
            self.ax1 = self.ax1 * 0.001 * 0.001
            self.ax2 = self.ax2 * 0.001 * 0.001
            self.unit = new_unit
        elif self.unit == "mm" and new_unit == 'um':
            self.ax1 = self.ax1 * 1000
            self.ax2 = self.ax2 * 1000
            self.unit = new_unit
        elif self.unit == "mm" and new_unit == 'm':
            self.ax1 = self.ax1 * 0.001
            self.ax2 = self.ax2 * 0.001
            self.unit = new_unit
        elif self.unit == "m" and new_unit == 'um':
            self.ax1 = self.ax1 * 1000 * 1000
            self.ax2 = self.ax2 * 1000 *1000
            self.unit = new_unit
        elif self.unit == "m" and new_unit == 'mm':
            self.ax1 = self.ax1 * 1000
            self.ax2 = self.ax2 * 1000
            self.unit = new_unit
        elif self.unit == "um" and new_unit == 'um':
            pass
        else:
            print("Invalid unit given for point!")

    def print_point_information(self): 
        print("Point Information:")  
        print(f"{self.ax1_suffix}-Koordinate: {self.ax1}")
        print(f"{self.ax2_suffix}-Koordinate: {self.ax2}")
        print(f"Unit: {self.unit}")

class Line:
    def __init__(self, Point_1:Point, Point_2:Point, unit):
        self.Point_1 = copy.copy(Point_1)
        self.Point_2 = copy.copy(Point_2)
        self.unit = unit
        self.__set_axis_suffix__()
        self.change_unit_to(unit)

    def __set_axis_suffix__(self):
        if (self.Point_1.ax1_suffix is not self.Point_2.ax1_suffix) or (self.Point_1.ax2_suffix is not self.Point_2.ax2_suffix):
            print("WARNING: You are trying to create a line from two points that are given in different coordinate systems! It will be assumed that Point 2 is given in CS of Point 1.")
            self.Point_2.ax1_suffix = self.Point_1.ax1_suffix
            self.Point_2.ax2_suffix = self.Point_1.ax2_suffix
        else:
            self.ax1_suffix = self.Point_1.ax1_suffix
            self.ax2_suffix = self.Point_1.ax2_suffix

    def change_unit_to(self,new_unit):   
        self.Point_1.change_unit_to(new_unit)
        self.Point_2.change_unit_to(new_unit)
        self.unit=new_unit

    def print_Line_information(self):
        print("Point 1:")
        self.Point_1.print_point_information()
        print("Point 2:")
        self.Point_2.print_point_information()

if __name__ == "__main__":
    mycircle=Circle(5, 5, 1, 'x','y', 'mm')
    mypoint_1=Point(5,1,'x','y','um')
    mypoint_2=Point(8,3,'x','y','um')
    myline=Line(mypoint_1,mypoint_2,'um')
    myline.print_Line_information()
    mycircle.print_circle_information()
    mypoint_1.change_unit_to("mm")
    mypoint_1.print_point_information()
    
