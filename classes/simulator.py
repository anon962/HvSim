from .entities import Player, MonsterList
from .logger import Logger
from queue import PriorityQueue


class Simulator(Logger):
	def __init__(self, loadout=None, style=None):
		self.player= Player(sim=self, loadout=loadout, style=style)
		self.time= 0

		# round-specific attrs -- just so they don't have to be passed as function params
		self.queue= None
		self.mob_list= None

		super().__init__(__name__)


	def test(self):
		for i in range(1):
			self.play_round(3)

	# simulate single round
	@Logger.add_tags("round_info")
	def play_round(self, n):
		# spawn mobs
		self.mob_list= MonsterList(sim=self, n=n)
		self.info(self.render_template("spawn", SELF=self))

		# initialize queue
		self.queue= PriorityQueue()
		self._qput(self.player)
		for x in self.mob_list:
			self._qput(x)

		# start combat
		while any(x.alive() for x in self.mob_list) and self.player.alive():
			self._qcheck()

	# queue up action
	def _qput(self, entity):
		self.queue.put((entity.next_action_time, entity))

	# do action then re-queue
	def _qcheck(self):
		# inits
		entity= self.queue.get()[1]
		if isinstance(entity, Player):
			self.info(self.render_template("turn_divider", SELF=self))

		# check if alive
		if not entity.alive():
			return

		# do action
		entity.do_battle()

		# check if alive
		if not entity.alive():
			return

		# re-queue
		self._qput(entity)


if __name__ == "__main__":
	Simulator().test()