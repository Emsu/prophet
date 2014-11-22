.. _best_practices:

Best Practices
==============

Try to keep as much of your code as possible in the pandas (or numpy) space. Lots of smart folk have spent a considerable amount of time optimizing those libaries. Since most of the code in pandas and numpy is executed in C, it will be much more performant.

For the data generators, please pass arround panadas Dataframes as much as possible. (Which then means that your order generator will have to operate on pandas Dataframes)
