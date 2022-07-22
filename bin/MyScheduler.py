from pyAmakCore.classes.scheduler_mono_threading import SchedulerMono


class myScheduler(SchedulerMono):
    def run(self) -> None:
        for _ in range (200):
            print("Cycle : ", self.amas.get_cycle())

            if self.exit_bool:
                break


            self.first_part()
            self.main_part()
            self.last_part()
        self.__close_child()

    