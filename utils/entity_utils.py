import functools # preserve function name

def cooldown(n):
	def decorator(func):
		@functools.wraps(func)
		def wrapper(self,*args,**kwargs):
			# do action
			assert self.cooldowns.get(func.__name__, 0) == 0
			func(self,*args,**kwargs)

			# decrement cooldowns
			for x in self.cooldowns:
				self.cooldowns[x]-= 1
			self.cooldowns= { x:y for x,y in self.cooldowns.items() if y > 0 }

			# add cooldown
			if n > 0:
				self.cooldowns[func.__name__]= n
		return wrapper
	return decorator

def action_time(base_time):
	def decorator(func):
		@functools.wraps(func)
		def wrapper(self,*args,**kwargs):
			t= base_time * self['speed']

			# do action
			func(self,*args,**kwargs)
			self.next_action_time+= t

			# decrement buff durations
			tmp= self.next_action_time
			ticks= int(tmp+t) - int(tmp)

			for i in range(ticks):
				for x in self.buffs:
					x.tick()
				self.buffs.clear_expired()

			# apply regeneration
			self.natural_regen()
		return wrapper
	return decorator
