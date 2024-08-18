# Creating your first app

Creating apps can be difficult, but with ScriptBlocks, it is way easier to create apps from scratch. Here's how you do it:

First, open your ScriptBlocks project, if applicable. Then, look at the main pane in the middle - that's where we are going to type our code. Next, type the following code - this is basic boilerplate code for our app:

```py
import scriptblocks

app = scriptblocks.App()
app.name = "My first app!"
app.version = "v1.0.0-alpha.1"
app.author = "OmgRod"

app.render()
```

Let's go through the code now:

- Line 3 initialises the app
- Lines 4-6 set the info about the app
- Line 8 creates the app window

This is it for creating apps so now, let's move on to Object Management.