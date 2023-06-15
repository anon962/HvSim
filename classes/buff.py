from abc import abstractmethod
from .logger import Logger
import utils


class Buff(Logger):
	def __init__(self, entity):
		self.name= self.__class__.__name__
		self.config= utils.load_yaml(utils.BUFF_CONFIG)[self.name.lower()]

		self.duration= self.config['duration']
		self.entity= entity
		self.on_apply()

		super().__init__(__name__)
		self.add_tags(self.name)

	def expired(self):
		return self.duration <= 0

	def tick(self):
		if self.duration > 0:
			self.duration-= 1
			self.on_tick()

			if self.duration == 0:
				self.on_expire()

	@abstractmethod
	def on_tick(self):
		...

	def on_apply(self):
		self.info(self.render_template("buff_apply", buff=self))

	def on_expire(self):
		self.info(self.render_template("buff_expire", buff=self))