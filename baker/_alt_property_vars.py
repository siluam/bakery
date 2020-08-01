class _alt_property_vars:

	@property
	def _run(self):
		return self.__run

	@_run.setter
	def _run(self, value):
		if value:
			self._capture = "run"

	@property
	def _list(self):
		return self.__list

	@_list.setter
	def _list(self, value):
		if value:
			self._type = list