#### Interact with Python
#### Construct connection with MySQL and retrieve data
#### Visulize data using ggplot

library("RMySQL")
library("ggplot2")

con <- dbConnect(MySQL(), user="root", password="",
                  dbname="DB", host="localhost")

mydata <- dbReadTable(con, "mydata")

# Bubble Chart for Expenditure on Education, Fertility Rate and GDP per Capita
ggplot(mydata, aes(x=Expenditure_on_Education, y=Fertility_Rate, size=GDP, label=Country))+
  geom_point(colour="white", fill="red", shape=21)+ 
  scale_size_area(breaks=c(250, 500, 1000, 10000, 40000), "GDP per capita\n(constant 2005 US$)",max_size = 25)+
  stat_smooth(method="lm", size=0.5, colour="black", alpha=0.4, level=0.95)+
  scale_x_continuous(name="Public spending on education, total (% of GDP)", limits=c(0,8))+
  scale_y_continuous(name="Fertility rate, total (births per woman)", limits=c(1,7))+
  geom_text(size=4)+
  ggtitle("Fertility Rate v.s. Expenditure on Education") +
  theme_bw()

# Bar Chart for Fertility rate and Region, sorted by Fertility rate
ggplot(data=mydata, aes(reorder(factor(Country),-Fertility_Rate),y=Fertility_Rate, fill=Region)) + geom_bar(stat="identity")+
  scale_x_discrete(name='Country') + ggtitle("Fertility Rate by Region") + 
  theme(title = element_text(size=rel(1.2)), axis.text.x = element_text(size = rel(1.8), angle = 90, hjust = 1))

# Bar chart for Fertility rate and income level, sorted by Fertility rate
ggplot(data=mydata, aes(reorder(factor(Country),-Fertility_Rate),y=Fertility_Rate, fill=Income_Level)) + geom_bar(stat="identity")+
  scale_x_discrete(name='Country') + ggtitle("Fertility Rate by Income Level") + 
  theme(title = element_text(size = rel(1.2)), axis.text.x = element_text(size = rel(1.8), angle = 90, hjust = 1))
