[Chinese Version](https://github.com/rosstzc/koudai/blob/master/README_CH.MD)

[English Version](https://github.com/rosstzc/koudai/blob/master/README.md)

# analysis of the pocket pivot signal and sectors 
This project is to count the number of stocks  with the pocket pivot signal in each sector every day.  After a while, we will get a trend of the number of stocks signals for each sector. It helps us to know if a stock sector is going bullish or not.



## keyword Description

- Pocket pivot: It refers to a kind of price pattern of a stock. The pocket pivot is a signal that is computed according to certain rules, and is usually used as a signal indicator of a strong trend.
- Stock sectors: A stock sector is a group of stocks that have a lot in common, usually they are in similar industries, similar concepts, etc.
- TDX: a well-known stock analysis software in China, supports various graphic analysis and  customization functions, etc.
- Tableau: a professional tool for data analysis and visualization.

## Project Introduction

On the stock market (there are 3~4 thousand stocks on the China stock market),  each stock will be classified into one or more sectors according to its concept and industry. There are more than 300 stock sectors in TDX (a stock software in China). Each day, there will be some stocks that have the pocket pivot signal. This project is to count the number of stocks  with signals in each sector every day.  After a while, we will get a trend of the number of stocks signals for each sector. It helps us to know if a stock sector is going bullish or not.

This project is to count the number of stocks  with the pocket pivot signal in each sector every day.  After a while, we will get a trend of the number of stocks signals for each sector. It helps us to know if a stock sector is going bullish or not.

### Thinking in the project

I used to use TDX, as a filter tool for pocket pivot stocks. When I wanted to know the number of pocket pivot stocks in sectors, I found it could not be done directly in TDX. In theory, I can pick out the pocket pivot stocks in each sector. The problem is that it needs to run manually more than 300 times to get the result of all the sectors every day. It is too much work to do, and I had to think about other methods. After a while, I came up with a solution.  The step to implement below：

1. Exported the list of all sectors and the list of all stocks from TDX(include the sectors info which a stock belongs to), then computed to get the stock lists in each sector by Python.
2. Exported the list of stocks that have pocket pivot signals every day from TDX, then computed with the results of step1 to get the trend of the number of pivot stocks in each stock sector.
3. Used a data visualization tool to present the trend. (I used Tableau to visualize the data )

As to show the data in charts. Before I decided to use Tableau, I had learned about the drawing libraries in Python. It need more time to program  and the user experience is not as good as Tableau. So, I decided to use Tableau.

One more I want to say. In fact, I had thought about using python to get the pocket pivot stocks, instead of exporting from TDX. The process would be more automatically, because it did not need to  exported data manually from TDX every day. But the problem was that the rule of pocket pivot stocks is complicated, and it would be time-consuming to implement in Python. So, I decided to process the data separately.

### Use of Technology in Project:

1. Panda library for precessing and analyzing the data
2. Tableau for data visualization

### Experience from Project

This was my personal project that satisfied my goal of analyzing the stock sectors. The main code of the project was about 200 lines, which is focus on processing data. It had no complicate logic. The hard parts of the project was that which data should be processed by what kind of method or tool. 

In general, I think that the main task of tool project is to achieve the goal in a short time, and the second is considering the usability and maintainability. Although this project involved 3 tools, but it was the easiest solution to achieve the goal in my mind.

### Precautions:

This project was a complete development project that can be run directly. The functional logic based on my idea, and other may not apply. If you are interested in this project , you can download and check it, to extract some value of the codes or idea.

### Some screenshots of the project:

1 The figure below shows the output data of the project. The data includes the number of stocks with the pocket pivot signal in each sector every day.
![koudai1](https://user-images.githubusercontent.com/5052733/201505176-509041a7-332a-4165-9a4d-a156e41d2b18.png)



2 The figure below shows the trend of the number of stocks with pocket pivot signal in a stock sector.
![2 指定板块的支点数走势](https://user-images.githubusercontent.com/5052733/201504688-c6faee74-5f38-48bc-adf6-68e19cf91201.png)

3 The figure below shows the sequence of stock sectors according to the proportion of pivot stocks on a certain day.
![按日期查看支点比例排序](https://user-images.githubusercontent.com/5052733/201504819-e884a1b5-0208-401d-b190-06a63079e7e7.png)

4 The figure below shows the related sectors of the pivot stocks.
![当天支点所在板块的支点走势](https://user-images.githubusercontent.com/5052733/201504865-b13e3f7c-d841-4d84-8cf3-55dde97ee3fb.png)
