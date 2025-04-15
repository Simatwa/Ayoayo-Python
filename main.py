#!/usr/bin/python

from typing import List, Optional, Union


class Player:
    """
    Represents a player in the game.

    Attributes:
        _name (str): The name of the player.
        _player_num (int): The player's number or identifier (0 or 1).
        _store (int): The player's store for holding seeds.
    """

    def __init__(self, name: str, player_num: int) -> None:
        """
        Initializes a Player instance.

        Args:
            name (str): The name of the player.
            player_num (int): The player's number (0 or 1).
        """
        self._name = name
        self._player_num = player_num
        self._store = 0

    def get_name(self) -> str:
        """
        Retrieves the name of the player.

        Returns:
            str: The name of the player.
        """
        return self._name

    def get_store(self) -> int:
        """
        Retrieves the current number of seeds in the player's store.

        Returns:
            int: The number of seeds in the store.
        """
        return self._store

    def add_to_store(self, seeds: int) -> None:
        """
        Adds seeds to the player's store.

        Args:
            seeds (int): The number of seeds to add to the store.
        """
        self._store += seeds


class Ayoayo:
    """
    Represents the Ayoayo game.

    Attributes:
        _players (List[Optional[Player]]): List of players in the game (indices 0 and 1).
        _board (List[List[int]]): The game board with pits for each player.
        _game_ended (bool): Indicates whether the game has ended.
    """

    def __init__(self) -> None:
        """
        Initializes the Ayoayo game with default settings.
        """
        self._players: List[Optional[Player]] = [
            None,
            None,
        ]  # Index 0 for player1, 1 for player2
        self._board: List[List[int]] = [
            [4, 4, 4, 4, 4, 4],  # Player 0 pits
            [4, 4, 4, 4, 4, 4],  # Player 1 pits
        ]
        self._game_ended: bool = False

    def createPlayer(self, name: str) -> Player:
        """
        Creates a new player and assigns them to the game.

        Args:
            name (str): The name of the player.

        Returns:
            Player: The created player instance.
        """
        player_num = 0 if self._players[0] is None else 1
        player = Player(name, player_num)
        self._players[player_num] = player
        return player

    def printBoard(self) -> None:
        """
        Prints the current state of the game board.
        """
        if not all(self._players):
            print("Players not initialized yet")
            return

        print("player1:")
        print(f"store: {self._players[0].get_store()}")
        print(self._board[0])
        print("player2:")
        print(f"store: {self._players[1].get_store()}")
        print(self._board[1])

    def returnWinner(self) -> str:
        """
        Determines the winner of the game.

        Returns:
            str: The winner's name or a message indicating a tie or ongoing game.
        """
        if not self._game_ended:
            return "Game has not ended"

        p1_score = self._players[0].get_store()
        p2_score = self._players[1].get_store()

        if p1_score > p2_score:
            return f"Winner is player 1: {self._players[0].get_name()}"
        elif p2_score > p1_score:
            return f"Winner is player 2: {self._players[1].get_name()}"
        else:
            return "It's a tie"

    def playGame(self, player_index: int, pit_index: int) -> Union[str, List[int]]:
        """
        Executes a turn for the specified player.

        Args:
            player_index (int): The index of the player (0 or 1).
            pit_index (int): The index of the pit (1-6).

        Returns:
            Union[str, List[int]]: A message or the current board state.
        """
        if self._game_ended:
            return "Game is ended"

        if player_index not in (0, 1):
            return "Invalid player index"

        if pit_index <= 0 or pit_index > 6:
            return "Invalid number for pit index"

        pit_index -= 1  # Convert to 0-based index

        # Check if pit is empty
        if self._board[player_index][pit_index] == 0:
            return "Invalid move - pit is empty"

        # Collect seeds from the pit
        seeds_to_sow = self._board[player_index][pit_index]
        self._board[player_index][pit_index] = 0

        current_player = player_index
        current_pit = pit_index
        last_seed_in_store = False

        # Sow the seeds
        while seeds_to_sow > 0:
            # Move to next pit
            current_pit += 1

            # Handle wrap-around and stores
            if current_pit >= 6:
                if current_player == player_index:
                    # Add to own store
                    self._players[player_index].add_to_store(1)
                    seeds_to_sow -= 1

                    # Check if last seed
                    if seeds_to_sow == 0:
                        last_seed_in_store = True
                        break

                current_player = 1 - current_player  # Switch player (0->1, 1->0)
                current_pit = -1  # Will be incremented to 0 next iteration
                continue

            # Add seed to pit
            self._board[current_player][current_pit] += 1
            seeds_to_sow -= 1

        # Check for extra turn or capture
        if last_seed_in_store:
            print(f"player {player_index + 1} take another turn")
        elif (
            current_player == player_index
            and self._board[current_player][current_pit] == 1
        ):
            # Capture - last seed landed in empty pit on own side
            opposite_pit = 5 - current_pit
            captured_seeds = self._board[1 - current_player][opposite_pit]
            if captured_seeds > 0:
                total_captured = (
                    captured_seeds + 1
                )  # The capturing seed + opposite seeds
                self._players[player_index].add_to_store(total_captured)
                self._board[current_player][current_pit] = 0
                self._board[1 - current_player][opposite_pit] = 0

        # Check if game has ended
        self._check_game_end()

        # Return current board state
        return self._get_board_state()

    def _check_game_end(self) -> None:
        """
        Checks if the game has ended and updates the game state.
        """
        # Game ends when one player has no seeds left in their pits
        p0_has_seeds = any(seeds > 0 for seeds in self._board[0])
        p1_has_seeds = any(seeds > 0 for seeds in self._board[1])

        if not p0_has_seeds or not p1_has_seeds:
            self._game_ended = True
            # Collect remaining seeds
            remaining_p0 = sum(self._board[0])
            remaining_p1 = sum(self._board[1])

            self._players[0].add_to_store(remaining_p0)
            self._players[1].add_to_store(remaining_p1)

            # Clear the pits
            self._board[0] = [0] * 6
            self._board[1] = [0] * 6

    def _get_board_state(self) -> List[int]:
        """
        Retrieves the current state of the game board.

        Returns:
            List[int]: The current board state including pits and stores.
        """
        return [
            *self._board[0],  # Player 0 pits 1-6
            self._players[0].get_store(),  # Player 0 store
            *self._board[1],  # Player 1 pits 1-6
            self._players[1].get_store(),  # Player 1 store
        ]


if __name__ == "__main__":
    # Example 1 from the requirements (adjusted for 0-based player indices)
    print("Example 1:")
    game1 = Ayoayo()
    player1 = game1.createPlayer("Jensen")
    player2 = game1.createPlayer("Brian")

    print(game1.playGame(0, 3))  # Player 1 (index 0) moves
    game1.playGame(0, 1)
    game1.playGame(1, 3)  # Player 2 (index 1) moves
    game1.playGame(1, 4)
    game1.playGame(0, 2)
    game1.playGame(1, 2)
    game1.playGame(0, 1)
    game1.printBoard()
    print(game1.returnWinner())
    print("\n")

    # Example 2 from the requirements (adjusted for 0-based player indices)
    print("Example 2:")
    game2 = Ayoayo()
    player1 = game2.createPlayer("Jensen")
    player2 = game2.createPlayer("Brian")

    game2.playGame(0, 1)
    game2.playGame(0, 2)
    game2.playGame(0, 3)
    game2.playGame(0, 4)
    game2.playGame(0, 5)
    game2.playGame(0, 6)
    game2.printBoard()
    print(game2.returnWinner())
    print("\n")

    # Additional test cases
    print("Additional Test Cases:")
    game3 = Ayoayo()
    p1 = game3.createPlayer("Alice")
    p2 = game3.createPlayer("Bob")

    # Test invalid player index
    print(game3.playGame(2, 1))  # Should return "Invalid player index"
    print(game3.playGame(-1, 1))  # Should return "Invalid player index"

    # Test invalid pit index
    print(game3.playGame(0, 0))  # Should return "Invalid number for pit index"
    print(game3.playGame(0, 7))  # Should return "Invalid number for pit index"

    # Test empty pit move
    game3.playGame(0, 1)  # Take all seeds from pit 1
    print(game3.playGame(0, 1))  # Should return "Invalid move - pit is empty"

    # Test capture scenario
    game3.playGame(1, 3)  # Player 2 moves
    game3.playGame(0, 2)  # Player 1 moves - might set up capture
    game3.playGame(1, 6)  # Player 2 moves
    # Player 1 might now have a capture opportunity
    game3.printBoard()
    print(game3.playGame(0, 3))  # Potential capture move
    game3.printBoard()
