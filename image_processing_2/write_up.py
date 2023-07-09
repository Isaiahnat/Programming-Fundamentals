from lab import *
# code in this block will only be run when you explicitly run your script,
# and not when the tests are being run.  this is a good place for
# generating images, etc.

# cat = load_color_image("test_images/cat.png")
# color_inverted = color_filter_from_greyscale_filter(inverted)
# inverted_color_cat = color_inverted(cat)
# print(inverted_color_cat)
# save_color_image(inverted_color_cat, "inverted_color_cat.png")

# python = load_color_image("test_images/python.png")
# x = make_blur_filter(9)
# blur = color_filter_from_greyscale_filter(x)
# blurred_color_python = blur(python)
# save_color_image(blurred_color_python, "blurred_color_python.png")

sparrow = load_color_image("test_images/sparrowchick.png")
x = make_sharpen_filter(7)
sharpen = color_filter_from_greyscale_filter(x)
sharpened_color_sparrow = sharpen(sparrow)
save_color_image(sharpened_color_sparrow, "sharpened_color_sparrow.png")

# frog = load_color_image("test_images/frog.png")
# filter1 = color_filter_from_greyscale_filter(edges)
# filter2 = color_filter_from_greyscale_filter(make_blur_filter(5))
# filt = filter_cascade([filter1, filter1, filter2, filter1])
# cascade_frog = filt(frog)
# save_color_image(cascade_frog,"cascade_frog.png")

# pattern = {'height': 4, 'width': 9, 'pixels': [200, 160, 160, 160, 153, 160, 160, 160, 200, 200, 160, 160, 160, 153, 160, 160, 160, 200, 0, 153, 160, 160, 160, 160, 160, 153, 0, 0, 153, 153, 160, 160, 160, 153, 153, 0]}
# print(minimum_energy_seam(cumulative_energy_map(compute_energy(pattern))))

# twocats = load_color_image("test_images/twocats.png")
# seam_carved_cats = seam_carving(twocats,100)
# save_color_image(seam_carved_cats,"seam_carved_cats.png")

# bluegill = load_color_image("test_images/bluegill.png")
# warm_bluegill = custom_feature(bluegill, "warm", 0.7)
# save_color_image(warm_bluegill, "warm_bluegill.png")