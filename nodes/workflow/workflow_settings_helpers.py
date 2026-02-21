# (c) TenserTensor || Apache-2.0 (apache.org/licenses/LICENSE-2.0)

import math

import torch


def _compute_empirical_mu(image_seq_len, num_steps):
    a1, b1 = 8.73809524e-05, 1.89833333
    a2, b2 = 0.00016927, 0.45666666

    if image_seq_len > 4300:
        mu = a2 * image_seq_len + b2
        return float(mu)

    m_200 = a2 * image_seq_len + b2
    m_10 = a1 * image_seq_len + b1

    a = (m_200 - m_10) / 190.0
    b = m_200 - 200.0 * a
    mu = a * num_steps + b

    return float(mu)


def _generalized_time_snr_shift(t, mu, sigma):
    return math.exp(mu) / (math.exp(mu) + (1 / t - 1) ** sigma)


def get_schedule(num_steps, width, height):
    image_seq_len = (width * height / (16 * 16))
    mu = _compute_empirical_mu(image_seq_len, num_steps)
    timesteps = torch.linspace(1, 0, num_steps + 1)
    timesteps = _generalized_time_snr_shift(timesteps, mu, 1.0)

    return (timesteps,)
