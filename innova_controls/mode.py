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

        self.heat = heat
        self.cool = cool
        self.dehumidify = dehumidify
        self.fan_only = fan_only
        self.auto = auto

    @property
    def is_heating(self) -> bool:
        return self.heat

    @property
    def is_cooling(self) -> bool:
        return self.cool

    @property
    def is_dehumidifying(self) -> bool:
        return self.dehumidify

    @property
    def is_fan_only(self) -> bool:
        return self.fan_only

    @property
    def is_auto(self) -> bool:
        return self.auto

    def __repr__(self) -> str:
        return (
            f"Mode(Code: {self.code}, Command: {self.command}, "
            f"Heat: {self.heat}, Cool: {self.cool}, Dehumidify: {self.dehumidify}, "
            f"Fan Only: {self.fan_only}, Auto: {self.auto})"
        )
