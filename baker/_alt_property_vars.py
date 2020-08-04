class _alt_property_vars:

	@property
	def _run(self):
		return self._capture == "run"

	@_run.setter
	def _run(self, value):
		if value:
			self._capture = "run"

	@property
	def _list(self):
		return self._type == list

	@_list.setter
	def _list(self, value):
		if value:
			self._type = list

	@property
	def _deck(self):
		return self._decorator

	@_deck.setter
	def _deck(self, value):
		self._decorator = bool(value)