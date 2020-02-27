## Q10- What’s the difference between Type I and Type II error?

More reading: Type I and type II errors (Wikipedia)

Don’t think that this is a trick question! Many machine learning interview questions will be an attempt to lob basic questions at you just to make sure you’re on top of your game and you’ve prepared all of your bases.

Type I error is a false positive, while Type II error is a false negative. Briefly stated, Type I error means claiming something has happened when it hasn’t, while Type II error means that you claim nothing is happening when in fact something is.

A clever way to think about this is to think of 

* _Type I error as telling a man he is pregnant_
* _while Type II error means you tell a pregnant woman she isn’t carrying a baby_

# Q13- What is deep learning, and how does it contrast with other machine learning algorithms?

More reading: Deep learning (Wikipedia)

Deep learning is a subset of machine learning that is concerned with neural networks: 
how to use backpropagation and certain principles from neuroscience to more accurately model large sets of unlabelled or semi-structured data. 
In that sense, deep learning represents an unsupervised learning algorithm that learns representations of data through the use of neural nets.


# Q15- What cross-validation technique would you use on a time series dataset?

More reading: Using k-fold cross-validation for time-series model selection [CrossValidated](https://stats.stackexchange.com/questions/14099/using-k-fold-cross-validation-for-time-series-model-selection)

Instead of using standard k-folds cross-validation, you have to pay attention to the fact that a time series is not randomly distributed data — it is inherently ordered by chronological order. If a pattern emerges in later time periods for example, your model may still pick up on it even if that effect doesn’t hold in earlier years!

You’ll want to do something like forward chaining where you’ll be able to model on past data then look at forward-facing data.

- fold 1 : training [1], test [2]
- fold 2 : training [1 2], test [3]
- fold 3 : training [1 2 3], test [4]
- fold 4 : training [1 2 3 4], test [5]
- fold 5 : training [1 2 3 4 5], test [6]

# Q20- When should you use classification over regression?

More reading: Regression vs Classification (Math StackExchange)

Classification produces discrete values and dataset to strict categories, while regression gives you continuous results that allow you to better distinguish differences between individual points. 
You would use classification over regression if you wanted your results to reflect the belongingness of data points in your dataset to certain explicit categories 
(ex: If you wanted to know whether a name was male or female rather than just how correlated they were with male and female names.)

# Q21- Name an example where ensemble techniques might be useful.

More reading: [Ensemble learning](https://en.wikipedia.org/wiki/Ensemble_learning)

Ensemble techniques use a combination of learning algorithms to optimize better predictive performance. 
They typically reduce overfitting in models and make the model more robust 
(unlikely to be influenced by small changes in the training data). 

You could list some examples of ensemble methods, from bagging to boosting to a “bucket of models” method 
and demonstrate how they could increase predictive power.