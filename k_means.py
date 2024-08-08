# LIbraries for plotting data and numpy arrays (NOTE: Outliers is my file made names outlier)
import numpy as np
import matplotlib.pyplot as plt
from Outliers import Outlier
import os
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from PIL import Image

"""
K means class that does k means and updates on i iterations
Updates the Silhouette coefficient, mid points and cluster points

"""
class K_means():

    """
    Intilizes variables 
    """
    def __init__(self,dp,cluster_count = 2,num_iterations = 15):

        # datapoints from outliers file to remove outlers and give points
        self.data_points = dp
        
        # number of clusters
        self.clusters = cluster_count

        # number of iterations
        self.iter = num_iterations

        # Dir to save combine imagies of points form angles
        self.dir_save = os.getcwd()

        # saves distances for euclidean and uses for assign to assign cluster
        self.distances = []

        # mid points of clusters
        self.mid = []

        # array of clusters of array of points
        self.clusters_points = None

        # gets just numbers from 0 to number of clusters as classfication of cluster
        self.unique = [i for i in range(cluster_count)]

        # Saves coefficent for early stoping if not imporvemnt after next iteration
        self.coefficent = None

    """
    Main function that runs for i-th iterations
    Obtains random mid points and every iteration updates euclidean 
    """
    def k_means(self):

        # random midpoints
        indices = np.random.choice(len(self.data_points), size= self.clusters, replace=False)

        # Assign midpoints to mid list
        for i in indices:
            
            # mid list
            self.mid.append(self.data_points[i])
        
        # iterations
        for i in range(self.iter):

            # print iteration
            print("iteration: ", i)

            # makes plot 
            self.plot(i)

            # Calculates euclidean
            self.euclidean()

            # assgins points to clusters
            self.assign()

            # Gets new midpoints
            self.mid_points()

            # calculates Silhouette coefficient
            s =  self.silhouette()

            # compares to see if any imporvement if none break
            if self.coefficent == s:
                break

            # make update of Silhouette coefficient variable
            self.coefficent = s
        
    """"
    mid point function to calucate mean and get middle of cluster
    """
    def mid_points(self):

        # goes through each cluster indivdually
        for cluster in range(len(self.clusters_points)):
            # starter values for each cluster
            sum_x = 0
            sum_y = 0
            sum_z = 0
            # loops through all points summing
            for x,y,z in self.clusters_points[cluster]:
                # sum variables
                sum_x += x
                sum_y += y
                sum_z += z

            # Gets mean of all x,y,z of cluster being looped
            x = sum_x / len(self.clusters_points[cluster])
            y = sum_y / len(self.clusters_points[cluster])
            z = sum_z / len(self.clusters_points[cluster])

            # hold array and updates new mid points in mid point array
            holder = np.array([x,y,z])
            self.mid[cluster] = holder

    
    """
    Assigns points to specific cluster
    """
    def assign(self):

        # Re-starts after every iteration
        self.clusters_points = [[] for _ in range(self.clusters)]

        # loops through number of points
        for number in range(len(self.data_points)):
        
            # holder for assigning point to cluster
            cluster_number = -1

            # hold nearest value out of the k th clusters
            nearest = float("inf")

            # loops through calucated distances 
            for dist in range(len(self.distances)):
                
                # obtains distance
                holder = self.distances[dist][number]
                
                # chackes nearest and assigns to cluster variable and saves nearest
                if holder < nearest:

                    nearest = holder
                    cluster_number = dist
            
            # assigns point to cluster
            self.clusters_points[cluster_number].append(self.data_points[number])

    """
    Caluclating Euclidena distance
    """
    def euclidean(self):

        # new distances restart after every iteration
        self.distances = []

        # takes mid points
        for x1,y1,z1 in self.mid:
            
            # holder for that spcific mid point
            dists = []

            # loop through points
            for x2,y2,z2 in self.data_points:
                
                # Calculates distances from midpoint
                holder = np.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

                # appended distance of point in 0 to end of data points
                dists.append(holder)    

            # After all have been done by midpoint append to distance where position is associated to self.mid  
            self.distances.append(dists)


    """
    Calculates silhoutte coefficent
    """
    def silhouette(self):
        
        # intilize sil
        sil = 0

        # loops thorugh clusters
        for cluster1 in self.clusters_points:
            
            # gets first point of cluster
            for x1,y1,z1 in cluster1:

                # intializers for in cluster and out of cluster with counting
                a = 0
                b = 0
                a_count = 0
                b_count = 0

                # loop through cluster
                for cluster2 in self.clusters_points:

                    # loop thorugh cluster points
                    for x2,y2,z2 in cluster2:
                        
                        # if clusters equal inside cluster
                        if np.array_equal(cluster1, cluster2):

                            a += np.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
                            a_count += 1

                        # else outside cluster
                        else:

                            b += np.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
                            b_count += 1

                # calulate Sil for that first point to everythigng
                a /= a_count
                b /= b_count

                # add sil for later for overall
                sil += (b - a) / max(a,b)

        # Overall avg off sil for all 
        silhouette_avg = sil / len(self.data_points)

        # prints sil
        print("Silhouette Score:", silhouette_avg)

        return silhouette_avg

    """
    Plots points in 3 dimensional and different angles
    """
    def plot(self, iteration):

        # obatins random colors for k th clusters
        colors = plt.cm.jet(np.linspace(0, 1, self.clusters))

        # intilizer
        fig = plt.figure()

        # subplot for bomine imagies
        ax = fig.add_subplot(111, projection='3d')

        # plots if just normal data no classification
        if self.clusters_points == None:
            
            # loops through data points
            for point in self.data_points:

                # Plots them
                ax.scatter(point[0], point[1], point[2], color='r')

        # if values are cluster plot clusters
        else:
            # the cluster number with assigned color
            for c, l in zip(colors, self.unique):
                
                # Plots nothing and assigns label
                ax.scatter([], [], [], color=c, label=l)  

                # loop through l cluster
                for point in self.clusters_points[l]:

                    # plots with color
                    ax.scatter(point[0], point[1], point[2], color=c)

        # adds  title and labels to plot
        ax.set_title("3D Scatter Plot")
        ax.set_xlabel("X Axis")
        ax.set_ylabel("Y Axis")
        ax.set_zlabel("Z Axis")
        ax.legend()

        # for storing all 4 angles of that iteration and clusters
        images = []

        # different angles
        for k in range(0, 180, 45):
            
            # rotates plot
            ax.view_init(elev=30, azim=k)
           
            # assigns and draw onto canvas with if imagie formating
            canvas = FigureCanvas(fig)
            canvas.draw()

            # makes sure imagie has color and correct height
            image = Image.frombytes('RGB', canvas.get_width_height(), canvas.tostring_rgb())

            # appends to imagie toi combine later
            images.append(image)

        # gets the total with of all imagie and hieight for scaling
        total_width = sum(image.size[0] for image in images)
        max_height = max(image.size[1] for image in images)

        # makes imagie of size of all for imagie height and width
        combined_im = Image.new('RGB', (total_width, max_height))
        
        # used to move the imagie so they are not piled on top of each other
        x_offset = 0

        # loops through pasteing plot onto combined imagie
        for image in images:
            
            # combines
            combined_im.paste(image, (x_offset, 0))

            # updates offset shifts right
            x_offset += image.size[0]

        # path and saves combined imagies
        combined_file_path = os.path.join(self.dir_save, "iteration_" + str(iteration) + "_combined_plots.png")
        combined_im.save(combined_file_path)


def main():


    # l = low, h = high, s = size for random points t = threshold for outliers
    s = Outlier(t_d=50, t_p=0.45)

    # Gets euclidean for outliers and have new set S
    s.euclidean()

    # prints outliers and new S
    s.print_outlier()
    s.print_new()

    # number of clusters
    num_cluster = 2

    # number of iterations
    num_i = 15
    
    # Starts K means dp gets new S, Cluster_count = # of clusters, number_iteraions = # of iteratiosn
    k = K_means(dp=s.get_new(),cluster_count=num_cluster,num_iterations=num_i)

    # starts k means clustering
    k.k_means()
    
if __name__ == "__main__":
    main()