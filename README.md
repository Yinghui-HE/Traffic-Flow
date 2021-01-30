# Traffic-Flow

**Introduction**

The Jefferson-Hoover intersection between the University of Southern California campus park and university village is an important transportation node. It is not only a must-go road for many students on school days, but also an important intersection that students, faculty, and local residents often drive through. However, before the COVID-19 broke out, this intersection was often congested, whether it was during the day or during the peak hours. We hope to help improve the traffic conditions in USC local communities through our project, so we chose to model this intersection and the adjacent crosswalk between the university village and university park. 
We constructed our model based on actual traffic light design, road speed limits, road length, and some other assumptions and tried different designs of traffic light durations to optimize the traffic flow by maximizing the number of cars leaving the studied area by the end of a simulation. To ensure quality and efficiency of the simulation program, we used object-oriented programming in python language by constructing a traffic light class and a road class. Further, we divided the road conditions into three scenarios according to the traffic volume and simulated and analyzed them separately. 
Our findings generally meet our expectations. Under different traffic conditions, we need to use different traffic light designs to maximize traffic flow, and roads with large traffic volumes require longer green light time. 


**Model**
We built a discrete-time model to simulate the traffic in our studied area using object-oriented programming. We took 1 second as our time step and simulated the traffic over a 20 ​minutes period and used the optimization method to find the traffic light strategy that maximizes the net traffic outflow, the number of cars leaving the studied area.
