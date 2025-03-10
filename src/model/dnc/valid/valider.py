from typing import List
import MrQLib as Lib

from src.model.error.printer import ErrorPrinter

class Valider:

    @staticmethod
    def valid(conn: Lib.MachineConnection, m_path: str, standard: str) -> bool:
        val_str = Lib.MemoryReader.Read(conn, m_path)
        return eval("{0} {1}".format(val_str, standard))

    @staticmethod
    def valid_multi_values(
        conn: Lib.MachineConnection, m_paths: List[str], standards: List[str]
    ) -> bool:
        if len(m_paths) != len(standards): 
            ErrorPrinter.print(
                "The length between memory path list and standard list is different.", 
                className=Valider.__name__
            )
            return False

        results = []
        for p,std in zip(m_paths, standards):
            results.append(Valider.valid(conn, p, std))
        
        return all(results)