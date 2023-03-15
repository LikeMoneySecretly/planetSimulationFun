# An optional additional project for a university module that I did a while ago
This system plots out some of the planets and attempts to timestep integrate their positions.

It doesn't work fully with satellite integration and I never got round to finishing that part off, but it acts as a cool way to see how I design my code. A lot of my later work is private due to a large amount of identifiable features and other code that could get me in trouble, this is just a nice thing that I can keep public without having to worry about what people might do with it :laugh:

# How to use
Control whether to display the total kinetic energies and other things in the projectTextFile, true/false. The satellite system doesn't work properly but the planetary motion system does.

The code generates the positions first then stores them and plots the result on an animation. I.e. the animation is displayed the code has already finished running.
This system is designed to use a Beeman step integration system to get relatively accurate results. Note, Some debugging print statements have been left in.
