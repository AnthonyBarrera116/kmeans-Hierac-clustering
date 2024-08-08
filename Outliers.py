# LIbraries for plotting data and numpy arrays 
import numpy as np
import matplotlib.pyplot as plt

"""
Get S' and removes outliers
"""
class Outlier():

    """
    Intilizes variables 
    """
    def __init__(self,low = 0,high = 25,t_d = 2,t_p = .40):

        # makes random 50 points for 10 groups made to get more ouside values or more diverse 
        points1 = np.random.uniform(0, 25, size=(50,3))
        points2 = np.random.uniform(25, 50, size=(50,3))
        points3 = np.random.uniform(50,75, size=(50,3))  
        points4 = np.random.uniform(75,100, size=(50,3))
        points5 = np.random.uniform(100,125, size=(50,3))
        points6 = np.random.uniform(0, 25, size=(50,3))
        points7 = np.random.uniform(25, 50, size=(50,3))
        points8 = np.random.uniform(50, 75, size=(50,3))
        points9 = np.random.uniform(75, 100, size=(50,3))
        points10 = np.random.uniform(100, 125, size=(50,3))

        # these are for offestting the valuse to move points away
        points6[:, 0] += 35
        points7[:, 0] += 35
        points7[:, 1] += 35
        points8[:, 0] -= 35
        points9[:, 0] -= 35
        points9[:, 1] += 35
        points10[:, 0] -= 40
        points10[:, 1] += 35


        # Combine the points
        self.data_points = np.vstack((points1,points2,points3,points4,points5,points6,points7,points8,points9,points10)).tolist()

        # saves outliers fro printing
        self.outliers = []

        # S'
        self.points_no_outliers = []

        # distance threshold
        self.thres_dis = t_d

        # percent threshold
        self.threshold_percent =t_p

    """
    Caluclating Euclidena distance
    """
    def euclidean(self):

        # loops through all points 
        for i1,point1 in enumerate(self.data_points):
            
            # ahodler for number of outliers that have gretaer distance from threshold
            greater = 0

            # gets values from point
            x2,y2,z2 = point1

            # loops through all values of data points
            for i2,point2 in enumerate(self.data_points):
                
                # obtains values from point2
                x1,y1,z1 = point2

                # calculates euclidean for checking distance threshold
                holder = np.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

                # checks if greater than thres
                if holder > self.thres_dis:
                    
                    # adds one if it is 
                    greater += 1             

            # takes total greater and divids by total points and checks percentage of if outlier
            if greater / len(self.data_points) >= self.threshold_percent:

                # appends to outlier
                self.outliers.append(point1)

            # appens to S'
            else:

                # S'
                self.points_no_outliers.append(point1)
    

    """
    Prints outlier
    """
    def print_outlier(self):

        # print title
        print("\n\n DATA OUTLIERS:")

        # For pretty printing outliers
        string = ""

        # for preety printing only 3 coordinates
        count = 0

        # loop through add to string and add newlines
        for point in self.outliers:

            # adding new line after 3 points
            if count == 3:
                string += "\n"
                count = 0
            
            # adds value to string and increases count
            string += str(point) + " "
            count +=1
    
        # print outliers and length
        print(string)
        print(len(self.outliers))

    """
    Prints S'
    """
    def print_new(self):

        # print title
        print("\n\n DATA WITHOUT OUTLIERS:")

        # For pretty printing S'
        string = ""

        # for preety printing only 3 coordinates
        count = 0

        # loop through add to string and add newlines
        for point in self.points_no_outliers:

            # adding new line after 3 points
            if count == 3:
                string += "\n"
                count = 0
            
            # adds value to string and increases count
            string += str(point) + " "
            count +=1

        # print outliers and length
        print(string)
        print(len(self.points_no_outliers))

    """
    returns outliers
    """
    def get_new(self):
        return self.points_no_outliers

    """
    makes a plot of outliers vs S'
    """
    def plot_data_3d(self):

        # intilize plot
        fig = plt.figure()

        # sizze of 3d plot
        ax = fig.add_subplot(111, projection='3d')

        # intlize label and color for data points no outliers
        ax.scatter([], [], [], c='b', label='Data Points')
        for x,y,z in self.points_no_outliers:
            ax.scatter(x,y,z, c='b')

        # intlize label and color for data points outliers 
        ax.scatter([], [], [], c='r', label='Outliers')
        for x,y,z in self.outliers:
            ax.scatter(x,y,z, c='r')

        # label graph
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Data Points with Outliers')
        ax.legend()

        # save figure to directory
        plt.savefig('Outliers vs S.png')


"""
Main
"""
def main():

    # t_d = thershold distance and t_p is therehold for outlier detection
    s = Outlier(t_d=75, t_p=0.45)
    
    #euclidean distance and removes outliers
    s.euclidean()
    
    # prints outliers and S'
    s.print_outlier()
    s.print_new()

    # Plots outliers vs S' and saves imagie
    s.plot_data_3d()
    
if __name__ == "__main__":
    main()