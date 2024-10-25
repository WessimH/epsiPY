from unittest import mock

import pytest

from reponse import *


def test_exo_1():
    # Patcher l'endroit où Thread est utilisé dans reponse.py (l'import exact)
    with mock.patch('reponse.threading.Thread', wraps=threading.Thread) as mock_thread:
        res = exo1(3)

        # Vérifier que 3 threads ont bien été créés
        assert mock_thread.call_count == 3

        # Vérifier que le résultat contient bien 3 threads créés
        assert res == ['Thread-1 (run)', 'Thread-2 (run)', 'Thread-3 (run)']

        # Vérifier que chaque thread a été démarré
        for thread in mock_thread.call_args_list:
            assert thread


def test_exo_2():
    numbers = [
        2, 3, 4, 5, 10, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
        1009, 1021, 1031, 1033, 1051, 1061, 1091, 1103, 1109, 1117, 1123,
        999983, 1000003, 1000033, 1000037, 1000081
    ]
    expected = [True, True, False, True, False, True, True, True, True, True, True, True, True,
                True, True, True, True, True, True, True, True, True, True, True, True, True, True,
                True, True, True, True]
    # Spy on the creation of multiprocessing.Process
    with mock.patch('reponse.multiprocessing.Pool', wraps=multiprocessing.Pool) as mock_process:
        result = exo2(numbers)

        # Assert that the correct number of processes were started
        assert mock_process.call_count >= 1  # Ensure at least one process is created

        # Validate the result
        assert result == expected


@pytest.mark.asyncio
async def test_exo_3():
    # Créer des instances de WaitAndValidateTask
    instance1 = WaitAndValidateTask()
    instance2 = WaitAndValidateTask()
    instance3 = WaitAndValidateTask()

    # Appel de la fonction process_tasks avec les instances
    await exo3([instance1, instance2, instance3])

    # Vérifier que start_time de chaque instance est très proche
    assert instance1.start_time is not None
    assert instance2.start_time is not None
    assert instance3.start_time is not None

    # Vérifier que la différence de temps entre les start_time est inférieure à 1 seconde
    times = [instance1.start_time, instance2.start_time, instance3.start_time]
    max_time = max(times)
    min_time = min(times)
    assert max_time - min_time < 1, "Les temps de début doivent être très proches (moins d'une seconde d'écart)"


def test_exo_4():
    pool = ProcessPool(3)
    with pool as queue:
        for i in range(100):
            queue.put(i)

    assert len(pool.get_results()) == 100  # Vérifie que 100 résultats ont été produits
