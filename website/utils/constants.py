TAILWIND_COLOR_CHOICES = [
    ('black', 'Black'),
    ('slate-100', 'Slate 100'),
    ('slate-200', 'Slate 200'),
    ('slate-600', 'Slate 600'),
    ('gray-600', 'Gray 600'),
    ('indigo-600', 'Blue 600'),
    ('red-600', 'Red 600'),
    ('transparent', 'Transparent'),
    ('white', 'White'),
]

"""
Note: as we're using tokenized class names to build the variations above in the ColorBlock
we need to make sure that the class names are valid here so that Tailwind can compile them and not tree shake them out.
# Text colors
text-black
text-gray-600
text-indigo-600
text-red-600
text-slate-100
text-slate-200
text-slate-600
text-transparent
text-white

# Background colors
bg-black
bg-gray-600
bg-indigo-600
bg-red-600
bg-slate-100
bg-slate-200
bg-slate-600
bg-transparent
bg-white
"""