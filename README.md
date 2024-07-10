# Background
This repo provides code that translates images into customizable cross-stitch patterns.
### Photography
From the generous gift of a Nikon N2000 film camera from my dear friend, Keiran, I discovered an appreciation for photography. Maybe it's the exhillerating fear of completely ruining a cannister of priceless memories when you try to switch out film rolls. Maybe it is the rush of smugness felt when saying "oh, I do film photography". Maybe it's simply the process of slowing down and thinking about the image you're about to capture. No matter the cause, I love my film pictures more than almost any I've captured digitally.

### Cross Stitch
I never expected to like cross-stitch but had so much fun with [my first kit](https://subversivecrossstitch.com/products/spark-joy-or-get-out) that I'm certain it will be a life-long hobby. My major issue with craft projects is that, in the end, I have a physical object I don't really need. Sure, I could run around, doing endless cross-stitches, making random things and either giving or throwing them away when they're done. But that is such a waste! Instead, I want to make something useful and meaningful, like a giant quilt of all of my favorite pictures. To do this, I simply wrote a program that will translate images into cross-stitch patterns. I can feed it my favorite images, enjoy the process of stitiching them, then combine everything into a gorgeous, sentimental guilt. Easy peasy!

### The Image to Cross-Stitch Pattern Program
In general, this project contains python code that transforms images of almost any kind into a scalable vector graphics (SVG) file containing a cross stitch pattern in black and white with symbols, color with symbols, and/or color without symbols. One of my favorite aspects of this program is that it matches colors in the images to specific DMC thread colors to use for each pattern. While I'll be the first to admit that it's not perfect, I'm incredibly happy with the result! 

# How to use
The first step is to make sure you have a CSV file that connects DMC thread colors to the RGB values of the thread. As this does not easily exist on the internet, [this script](DMC_color_scraping.py) will scrape the necessary information and create the CSV for you. 

With the DMC color mapping ready, you simply need to run the [main script](main.py) in your terminal `python main.py imagepath color_count method count` where you replace everything after `main.py` with your preferences. `imagepath` is the name of the image you want to make a pattern out of, `color_count` holds the number of unique colors you want to work with, `method` describes the color reduction method (kmeans, meanshift, or gmm), and `count` is the number of stitches you want on the x-axis of the pattern. 

Once the program has run, you'll see a results folder that holds the SVG pattern and color key. 

# Method
I am not, and will not pretend to be, an expert on web scraping and SVG formatting, so I will be more-or-less skimming that part of this repo. 

The [scraping code](DMC_color_scraping.py) works by accessing the HTML code of the table stored at the linked website, pulling out the values for each cell, and writing it to a CSV.

To start working with the program, you need to specify the image, the number of unique colors, the color reduction method, and the width in stitch count. With all of that information, the program loads and resizes the image. I used [a picture of champagne glasses at the top of the Eiffel Tower](eiffel_tower.png).

This resized image is then passed to a color reduction function that uses one of 3 methods to pick out a given number of unique colors for the image. These methods are described in brief:
1. K-Means: Partitions a dataset into k distinct clusters by initializing k centroids, assigning each data point to the nearest centroid, and updating the centroids based on the mean of the points in each cluster. This process repeats 15 times until the centroids stabilize, minimizing the within-cluster variance.

2. Mean Shift: Identifies clusters by iteratively shifting data points towards the mode (highest density point) of the dataset. It does so by defining a window around each data point, calculating the mean of the points within the window, and shifting the window to the mean. This process continues until convergence, resulting in clusters centered around areas of high data point density.

3. Gaussian Mixture Model: Models the dataset as a mixture of multiple Gaussian distributions, each representing a cluster. It uses the Expectation-Maximization (EM) algorithm to iteratively assign data points to clusters (Expectation step) and update the parameters of the Gaussian distributions (Maximization step) until convergence, allowing for clusters of varying shapes and sizes.

Once the color reduction step is done, the identified colors are mapped to their matching DMC thread color based on the euclidean distance of RBG values. A blank SVG template is initialized based on the image's dimensions and each cell is filled with the corresponding reference color. From there, a cleaning process occurs in which solitude pixels are smoothed out based on neighboring colors. 

Next, the SVG file is built cell-by-cell where each area is filled with either (or both) a color or symbol. You can see this in the [resulting image of my example](pattern.svg). [The key](key.svg) is then built after the pattern is done and it links color/symbol with specific DMC thread name. Both pattern and key files are saved in a seperate `results` folder. You then change the file names within this folder before running the program again with a different image. 

# Current Status
The code works in it's entirety and it does a pretty good job of producing recognizable patterns for a wide variety of images. Some images make better patterns than others, but I think that is a result of the resolution change and color reduction more than anything else. 

# Future direction - 7/9/24
I have noticed that relatively monochromatic images produce a very monochromatic pattern. One image is largely light blues and dusty sage greens with a hint of bright red and, when fed through my program, the red goes away completely in the pattern making process. This has to be because the red makes up a small percentage of pixel values and is deemed insignificant by the algorithm, but I wish it wouldn't do so. 

To fix this problem, my next step is to implement a saliency weighting algorithm in the color reduction methods that will retain a larger range of colors in the final pattern. OpenCV has functions for this, but I am not yet confident I understand how/why they work. My next update will include them!

