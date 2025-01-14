import math

class DimOrder(object):
	"""
	Represents the order of the dimensions in a dataset's shape.
	"""
	ChannelHeightWidth = ['c', 'h', 'w']
	HeightWidthChannel = ['h', 'w', 'c']


class panjareh(object):
	"""
	Represents a single window into a larger dataset.
	"""
	
	def __init__(self, x, y, w, h, dimOrder, transform = None):
		"""
		Creates a new window with the specified dimensions and transform
		"""
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.dimOrder = dimOrder
		self.transform = transform
	
	def apply(self, matrix):
		"""
		Slices the supplied matrix and applies any transform bound to this window
		"""
		view = matrix[ self.indices() ]
		return self.transform(view) if self.transform != None else view
	
	def getRect(self):
		"""
		Returns the window bounds as a tuple of (x,y,w,h)
		"""
		return (self.x, self.y, self.w, self.h)
	
	def setRect(self, rect):
		"""
		Sets the window bounds from a tuple of (x,y,w,h)
		"""
		self.x, self.y, self.w, self.h = rect
	
	def indices(self, includeChannel=True):
		"""
		Retrieves the indices for this window as a tuple of slices
		"""
		if self.dimOrder == DimOrder.HeightWidthChannel:
			
			# Equivalent to [self.y:self.y+self.h+1, self.x:self.x+self.w+1]
			return (
				slice(self.y, self.y+self.h),
				slice(self.x, self.x+self.w)
			)
			
		elif self.dimOrder == DimOrder.ChannelHeightWidth:
			
			if includeChannel is True:
				
				# Equivalent to [:, self.y:self.y+self.h+1, self.x:self.x+self.w+1]
				return (
					slice(None, None),
					slice(self.y, self.y+self.h),
					slice(self.x, self.x+self.w)
				)
				
			else:
				
				# Equivalent to [self.y:self.y+self.h+1, self.x:self.x+self.w+1]
				return (
					slice(self.y, self.y+self.h),
					slice(self.x, self.x+self.w)
				)
			
		else:
			raise Error('Unsupported order of dimensions: ' + str(self.dimOrder))
		
	def __str__(self):
		return '(' + str(self.x) + ',' + str(self.y) + ',' + str(self.w) + ',' + str(self.h) + ')'
	
	def __repr__(self):
		return self.__str__()


   if windowOverlapX is not None and windowOverlapY is not None:
        stepSizeX = windowSizeX - windowOverlapX
        stepSizeY = windowSizeY - windowOverlapY
    else:
        if overlapPercent is None:
            overlapPercent = 0.5  # Default overlap percentage, you can adjust this value as needed.
        stepSizeX = windowSizeX - int(math.floor(windowSizeX * overlapPercent))
        stepSizeY = windowSizeY - int(math.floor(windowSizeY * overlapPercent))
    
    # Determine how many windows we will need in order to cover the input data
    lastX = width - windowSizeX
    lastY = height - windowSizeY
    xOffsets = list(range(0, lastX + 1, stepSizeX))
    yOffsets = list(range(0, lastY + 1, stepSizeY))
    
    # Unless the input data dimensions are exact multiples of the step size,
    # we will need one additional row and column of windows to get 100% coverage
    if len(xOffsets) == 0 or xOffsets[-1] != lastX:
        xOffsets.append(lastX)
    if len(yOffsets) == 0 or yOffsets[-1] != lastY:
        yOffsets.append(lastY)
    
    # Generate the list of windows
    windows = []
    for xOffset in xOffsets:
        for yOffset in yOffsets:
            for transform in [None] + transforms:
                windows.append(SlidingWindow(
                    x=xOffset,
                    y=yOffset,
                    w=windowSizeX,
                    h=windowSizeY,
                    dimOrder=dimOrder,
                    transform=transform
                ))
    
    return windows


def generateRectanglarWindows(data, dimOrder, windowShape, overlapPercent, transforms=[]):
	"""
	Generates a set of sliding windows for the specified dataset, creating rectangular windows instead of square windows.
	`windowShape` must be a tuple specifying the desired window dimensions in (height,width) form.
	"""
	
	# Determine the dimensions of the input data
	width = data.shape[dimOrder.index('w')]
	height = data.shape[dimOrder.index('h')]
	
	# Generate the windows
	windowHeight, windowWidth = windowShape
	return generateForSize(
		width,
		height,
		dimOrder,
		0,
		overlapPercent,
		transforms,
		overrideWidth = windowWidth,
		overrideHeight = windowHeight
	)


def generateForNumberOfWindows(data, dimOrder, windowCount, overlapPercent, transforms=[]):
	"""
	Generates a set of sliding windows for the specified dataset, automatically determining the required window size in
	order to create the specified number of windows. `windowCount` must be a tuple specifying the desired number of windows
	along the Y and X axes, in the form (countY, countX).
	"""
	
	# Determine the dimensions of the input data
	width = data.shape[dimOrder.index('w')]
	height = data.shape[dimOrder.index('h')]
	
	# Determine the window size required to most closely match the desired window count along both axes
	countY, countX = windowCount
	windowSizeX = math.ceil(width / countX)
	windowSizeY = math.ceil(height / countY)
	
	# Generate the windows
	return generateForSize(
		width,
		height,
		dimOrder,
		0,
		overlapPercent,
		transforms,
		overrideWidth = windowSizeX,
		overrideHeight = windowSizeY
	)
