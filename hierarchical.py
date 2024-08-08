# LIbraries for plotting data and numpy arrays (NOTE: Outliers is my file made names outlier)
import numpy as np
import matplotlib.pyplot as plt
from Outliers import Outlier
import os
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from PIL import Image


"""
Hierarchical means class 
Updates the Silhouette coefficient and cluster points

"""
class Hierarchical():

    """
    Intilizes variables 
    """
    def __init__(self,dp,k=2):

        # datapoints from outliers file to remove outlers and give points
        self.data_points = dp

        # Dir to save combine imagies of points form angles
        self.dir_save = os.getcwd()

        # make indivdual clusters from data points
        self.clusters_made = [[x] for x in self.data_points]

        # Number of clusters user wants
        self.threshold_k = k

        # makes matrix of distance of all points. Make infinite for all
        self.distances = None

        # for ploting and gets number of colors and assign cluster number with color
        self.unique = [i for i in range(k)]
    
    """
    Make matrix of distance from points
    """
    def euclidean(self,value):

        # value is either -inf or inf depending on choice of option of max or closet 
        self.distances = np.full((len(self.data_points), len(self.data_points)), value)
        
        # loops through points
        for i1,point1 in enumerate(self.data_points):
            
            # obtains point 1
            x1,y1,z1 = point1

            # loops through points again but the next point in self.datapoints
            for i2 in range(i1 + 1,len(self.data_points)):
                
                # obtains point 2
                x2,y2,z2 = self.data_points[i2]

                # calculates distance
                self.distances[i1][i2] = np.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
    
        #print(self.distances)


    """
    Merge at indices
    """
    def merge(self,i1,i2):
        # Merge the clusters indexs
        cluster1_index = None
        cluster2_index = None

        # loop through cluster to find datapoints cluster index for mergeing
        for cluster_index in range(len(self.clusters_made)):

            # if datapoint one is in cluster obtain cluster number
            if self.data_points[i1] in self.clusters_made[cluster_index]:

                # cluster index 1
                cluster1_index = cluster_index

            # if datapoint two is in cluster obtain cluster number
            if self.data_points[i2] in self.clusters_made[cluster_index]:
                    
                # cluster 2 index
                cluster2_index = cluster_index

        # checks if clusters are same since I don't update all points to be inf for points in cluster1 It just skips and sets it to inf
        if  cluster1_index != cluster2_index:

            # merges cluster and removes second
            self.clusters_made[cluster1_index].extend(self.clusters_made[cluster2_index])
            self.clusters_made.pop(cluster2_index)
            
        """
        matirx is size of datapoints by size of datapoints
        rather than updating two locations from the same distance anything under the diagional of 0.0 distance from point 1 point 1 will be inf
        """
        self.distances[i1][i2] = float('inf')

    """
    nearest clusters
    """
    def near(self):

        # Loop until the number of clusters reaches the threshold
        while len(self.clusters_made) > self.threshold_k:

            # gets smallest value in matrix
            smallest = np.min(self.distances)

            # Get indices 
            i1,i2 = np.where(self.distances == smallest)

            # indices of datapoints 
            i1,i2 = i1[0],i2[0]

            # merege cluster function
            self.merge(i1,i2)

    """
    farthest clusters
    """
    def far(self):

        # Loop until the number of clusters reaches the threshold
        while len(self.clusters_made) > self.threshold_k:

            # gets max distances at each point
            max_dist = []
            
            # loop through all datapoints and appends max values
            for point_index in range(len(self.data_points)):

                # appends max
                max_dist.append(np.max(self.distances[point_index]))

            # gets smallest value in max
            smallest_max = np.min(max_dist)

            # Get indices 
            i1,i2 = np.where(self.distances == smallest_max)

            # indices of datapoints 
            i1,i2 = i1[0],i2[0]

            # merege cluster function
            self.merge(i1,i2)

    """
    Get points and sums up values
    """
    def get_avg(self,c1,c2):

        # number from both clusters
        count = 0

        # total disctance between
        t_dist = 0

        # loop cluster 1 points
        for p1 in c1:

            # loop through cluster 2 points
            for p2 in c2:

                # add distance of points
                t_dist += self.distances[self.data_points.index(p1)] [self.data_points.index(p2)] 
                
                # add number of pairs
                count += 1

        # returns average distance
        return t_dist/ count

            
    """
    Avg clusters
    """
    def avg(self):

        # loop till number of clusters
        while len(self.clusters_made) > self.threshold_k:

            # for closest average distance
            closest = None

            # saves cluster indexs
            i1,i2 = None,None

            # loop through clusters
            for c1 in range(len(self.clusters_made)):

                # loop through 1 + clusster list
                for c2 in range(c1 + 1,len(self.clusters_made)):

                    # get average and saves to closets
                    dist = self.get_avg(self.clusters_made[c1],self.clusters_made[c2])

                    # saves to closet id closest average
                    if closest == None or dist < closest:

                        # saves to closest for comparing
                        closest = dist

                        # saves clusters indexs
                        i1,i2 = c1,c2

            # if they are not the saem since not all point in distance matrix are update and rather than change them i can just check if same cluster
            if  i1 != i2:

                # merges cluster and removes second
                self.clusters_made[i1].extend(self.clusters_made[i2])
                self.clusters_made.pop(i2)
            
            """
            matirx is size of datapoints by size of datapoints
            rather than updating two locations from the same distance anything under the diagional of 0.0 distance from point 1 point 1 will be inf
            """
            self.distances[i1][i2] = float('inf')

    """
    Get cluster center
    """
    def get_center_point_distance(self,c1,c2):

        # the average values for the 3 corrdinates of point1 and point2
        x1_center = 0
        y1_center = 0
        z1_center = 0
        x2_center = 0
        y2_center = 0
        z2_center = 0

        # gets center of cluster 1
        for p1 in c1:
            
            # gets coridinates x,y and z and adds
            x,y,z = p1
            x1_center += x
            y1_center += y
            z1_center += z

        # gets center of cluster 2
        for p2 in c2:

            # gets coridinates x,y and z and adds
            x,y,z = p2
            x2_center += x
            y2_center += y
            z2_center += z

        # divides all by lenght of cluster to get center of cluster
        x1_center /= len(c1)
        y1_center /= len(c1)
        z1_center /= len(c1)
        x2_center /= len(c2)
        y2_center /= len(c2)
        z2_center /= len(c2)

        # gets distance which will be used for getting smallest distance from center of clusters
        return np.sqrt((x2_center - x1_center)**2 + (y2_center - y1_center)**2 + (z2_center - z1_center)**2)

            
    """
    center clusters
    """
    def center(self):

        # loop till number of clusters
        while len(self.clusters_made) > self.threshold_k:

            # closest distance from cluster centers
            closest = None

            # cluster indexs
            i1,i2 = None,None

            # loop through clusters
            for c1 in range(len(self.clusters_made)):

                # loop through 1 + clusster list
                for c2 in range(c1 + 1,len(self.clusters_made)):

                    # gets centeroids distance between clusters
                    dist = self.get_center_point_distance(self.clusters_made[c1],self.clusters_made[c2])

                    # if none or the distance is smaller save to closest
                    if closest == None or dist < closest:

                        # closest centers distance for comparing
                        closest = dist

                        # saves clusters indexs
                        i1,i2 = c1,c2

            # if they are not the saem since not all point in distance matrix are update and rather than change them i can just check if same cluster
            if  i1 != i2:

                # merges cluster and removes second
                self.clusters_made[i1].extend(self.clusters_made[i2])
                self.clusters_made.pop(i2)
                #print(len(self.clusters_made))

            # Unlike other you need to update distance in this case we do it on the fly since the distance alwasy change when a point is added.

                
    """
    Clustering
    """
    def hierarchical(self,option):
        
        # plots data before clusters
        self.plot("before", True)  

        if option == 0:
            value = float('inf')
            # make matrrix of distance of all points only uses anything above the triangle since 4,5 would be the same as 5,4 where 5 5 would be zero
            self.euclidean(value)  
            self.near()

        elif option == 1:
            
            value = float('-inf')
            # make matrrix of distance of all points only uses anything above the triangle since 4,5 would be the same as 5,4 where 5 5 would be zero
            self.euclidean(value)
            self.far()
        
        elif option == 2:
            
            value = float('inf')
            # make matrrix of distance of all points only uses anything above the triangle since 4,5 would be the same as 5,4 where 5 5 would be zero
            self.euclidean(value)
            self.avg()
        
        elif option == 3:
            
            self.center()

        # returns silhoutte
        self.silhouette()

        # plots clusters
        self.plot("After", False)

    """
    Gets Silhoutte of clusters
    """
    def silhouette(self):
            
            # intilize sil
            sil = 0

            # loops thorugh clusters
            for cluster1 in self.clusters_made:
                
                # gets first point of cluster
                for x1,y1,z1 in cluster1:

                    # intializers for in cluster and out of cluster with counting
                    a = 0
                    b = 0
                    a_count = 0
                    b_count = 0

                    # loop through cluster
                    for cluster2 in self.clusters_made:

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
    def plot(self,title,normal):

        # obatins random colors for k th clusters
        colors = plt.cm.jet(np.linspace(0, 1, len(self.clusters_made)))

        # intilizer
        fig = plt.figure()

        # subplot for bomine imagies
        ax = fig.add_subplot(111, projection='3d')

        # plots if just normal data no classification
        if normal == True:

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
                for point in self.clusters_made[l]:

                    

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
        combined_file_path = os.path.join(self.dir_save, title + "_combined_plots.png")
        combined_im.save(combined_file_path)


def main():


    # t_d = thershold distance and t_p is therehold for outlier detection
    s = Outlier(t_d=100, t_p=0.45)
    
    #euclidean distance and removes outliers
    s.euclidean()
    
    # prints outliers and S'
    s.print_outlier()
    s.print_new()

    # Number of clusters
    k = 10

    """
    option 0: nearest points
    """
    h0 = Hierarchical(dp=s.get_new(),k = k)
    h0.hierarchical(0)

    """
    option 1: farthest points
    """
    h1 = Hierarchical(dp=s.get_new(),k = k)
    h1.hierarchical(1)

    """
    option 2: smallest average
    """
    h2 = Hierarchical(dp=s.get_new(),k = k)
    h2.hierarchical(2)

    """
    option 3: nearest centeroids
    """
    h3 = Hierarchical(dp=s.get_new(),k = k)
    h3.hierarchical(3)
    
if __name__ == "__main__":
    main()