import pandas as pd
def merge_datafram_function:
    sample = pd.read_csv("sampledatalive.csv")
    test = pd.read_csv("test 1-31-16.csv", encoding = "utf-16", skiprows=9, sep = '\t')
    return sample.join(test)
"""
Now that I have 10% of the line of code requirement for this assignment, I will use
the rest of the line-requirement to ask the following question and attempt to answer it:

what is the objective of this particular assignment? (the HW until now was great!)

What I perceive as the objectives:
    1 - to make progress toward the class group project.
    2 - to understand how a pull request works and to gain experience using pull
        requests in a collaborative setting.

    objective #1 is a great cause, we are learning how to work as a team toward
    completing a larger project and overcoming obstacles as they come up.

    objective #2 also has lots of added value toward our learning. This is
    an essential part of working collaboratively and using github.

This evaluation leads me to ask another question:
    WHY IS THERE A 50 LINE CODE REQUIREMNT FOR THIS ASSIGNMENT?!?!?!?

    I would like to point out to the fact that significant progress can be made
    toward the overall project with a single line of code (it took me 4 hours to
    figure out that enocding = "utf-16" is needed to read_csv), and that at the
    same time I can write 50 lines of malarkey without any value-added progress!

    The issue that I am having with my portion is to recreate mock data-set that
    will look like the final real data. currently the sample data doesnt have the
    correct entries (we will have sample name = date format: R 02/24/16 17:45),
    I am having trouble editing our file and saving it back into a readable csv.
    Instead of working toward solving the issue and making progress, I AM
    STRESSING OUT ABOUT HOW TO COMPLETE THE STUPID 50 LINES OF CODE!

    I want to point out another important fact: I am here (taking this class)
    because I want to learn how to use these very valuable computational tools.
    I am here because I want to become a better scientist.

    I AM NOT HERE BECAUSE I HAVE TO BE HERE! I am not here to be an academic
    mental-illness statistic, I am not here to be chronically anxious and stressed
    out.

    With this said, I would like to suggest that graduate students are most productive
    when they enjoy their subject as an art. We are here out of our own accord.
    We are passionate to learn and we expect to be treated like the self-respecting
    professionals that we are.

- Alexey Gilman
"""
