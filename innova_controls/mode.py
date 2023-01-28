class Mode:
    def __init__(
        self,
        command: str,
        code: int,
        heat: bool = False,
        cool: bool = False,
        dehumidify: bool = False,
        fan_only: bool = False,
        auto: bool = False,
    ) -> None:
        self.command = command
        self.code = code

        self._heat = heat
        self._cool = cool
        self._dehumidify = dehumidify
        self._fan_only = fan_only
        self._auto = auto

    @property
    def is_heating(self) -> bool:
        return self._heat

    @property
    def is_cooling(self) -> bool:
        return self._cool

    @property
    def is_dehumidifying(self) -> bool:
        return self._dehumidify

    @property
    def is_fan_only(self) -> bool:
        return self._fan_only

    @property
    def is_auto(self) -> bool:
        return self._auto

    def __repr__(self) -> str:
        return (
            f"Mode(Code: {self.code}, Command: {self.command}, "
            f"Heat: {self._heat}, Cool: {self._cool}, Dehumidify: {self._dehumidify}, "
            f"Fan Only: {self._fan_only}, Auto: {self._auto})"
        )
