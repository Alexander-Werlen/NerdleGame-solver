# NerdleGame-Solver
Using [information theory](https://en.wikipedia.org/wiki/Information_theory) we are able to find the best guess to make at any point. This repository stores the code needed to generate necessary data, and the code that solves the game using such data.

## How to solve the game
We want to minimize the amount of tries made to guess the equation. Therefore, with each guess, we should try to reduce as much as possible the amount of remaining equations that could be the answer.

When we make a guess, the matching pattern revealed gives us information about the answer. And it cuts down the amount of remaining equations that are possible answers. It is reasonable to assume that the expected amount of tries needed to guess the equation is proportional to the amount of remaining possible equations. As a consequence, we should always try to make a guess that maximizes the expected information we could get.

A common way to determine the expected information of a choice is by using the [Shanon entropy](https://en.wikipedia.org/wiki/Entropy_(information_theory)). Which is defined as:

$$H(X)=E_{X}[I_{x}]=-\sum_{x\in X}^{ }p(x)log(p(x))$$

The optimal guess is the one that maximizes the expected information. The solver programm computes the expected information of every possible guess using the Shanon entropy. Then it stores all the pairs *equation: ExpectedInfo* in a .txt file.