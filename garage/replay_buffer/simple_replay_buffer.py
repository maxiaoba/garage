"""This module implements a simple replay buffer."""
import numpy as np

from garage.misc.overrides import overrides
from garage.replay_buffer.base import ReplayBuffer


class SimpleReplayBuffer(ReplayBuffer):
    """
    This class implements SimpleReplayBuffer.

    It uses random batch sample to minimize correlations between samples.
    """

    def __init__(self, **kwargs):
        """Initialize the data used in SimpleReplayBuffer."""
        super(SimpleReplayBuffer, self).__init__(**kwargs)

    @overrides
    def sample(self, batch_size):
        """Sample a transition of batch_size."""
        # assert self._n_transitions_stored >= batch_size
        buffer = {}
        for key in self._buffer.keys():
            buffer[key] = self._buffer[key][:self._current_size]

        if self._n_transitions_stored > batch_size:
            # Select which episodes to use
            time_horizon = buffer["action"].shape[1]
            rollout_batch_size = buffer["action"].shape[0]
            episode_idxs = np.random.randint(rollout_batch_size, size=batch_size)
            # Select time steps to use
            t_samples = np.random.randint(time_horizon, size=batch_size)

            transitions = {}
            for key in buffer.keys():
                samples = buffer[key][episode_idxs, t_samples].copy()
                transitions[key] = samples.reshape(batch_size, *samples.shape[1:])

            assert (transitions["action"].shape[0] == batch_size)
        else:
            transitions = {}
            for key in buffer.keys():
                samples = buffer[key][:, :].copy()
                transitions[key] = samples.reshape(self._n_transitions_stored, *samples.shape[2:])

            assert (transitions["action"].shape[0] == self._n_transitions_stored)
        return transitions
