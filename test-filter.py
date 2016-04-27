import cairo
import numpy
import math

# Conclusion: filter BEST is good for scale < 2, then >=2 BILINEAR is probably better (smooth)
# Note, in our case, cairo uses software rendering (image-source.c)

def draw(scale, filtern):
    filter = getattr(cairo, "FILTER_" + filtern)

    im_data = numpy.zeros((32, 64, 4), dtype=numpy.uint8)
    im_data[:, :, 3] = 255
    im_data[::2, ::2] = 255 # every second pixel of second line is white
    im_format = cairo.FORMAT_RGB24

    height, width, _ = im_data.shape
    imgsurface = cairo.ImageSurface.create_for_data(im_data, im_format, width, height)
    surfpat = cairo.SurfacePattern(imgsurface)
    surfpat.set_filter(filter)

    outshape = (int(math.ceil(height * scale)), int(math.ceil(width * scale)), 4)
    im_out = numpy.zeros(outshape, dtype=numpy.uint8)
    outsurface = cairo.ImageSurface.create_for_data(im_out, cairo.FORMAT_ARGB32, outshape[1], outshape[0])
    ctx = cairo.Context(outsurface)
    ctx.scale(scale, scale)
    ctx.set_source(surfpat)
    # ctx.set_operator(blend_mode)
    ctx.paint()

    outsurface.write_to_png("filtered_%s_s_%s.png" % (filtern.lower(), scale))
    
    
for f in ("FAST", "GOOD", "BEST", "NEAREST", "BILINEAR"): # , "GAUSSIAN"
    for s in (0.4, 1, 1.1, 1.9, 2, 2.1, 4.11, 12.1, 33.1):
        draw(s, f)

