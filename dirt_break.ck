// dirt_break.ck

// Define the gain, noise, and filter
Gain g => ADSR env => BPF filter => dac;
Noise n => g;

// Set the gain level
g.gain(0.3);

// Set the envelope parameters
env.set(0.01, 0.1, 0.5, 0.1);

// Function to simulate the sound of breaking a dirt block with random filter modulation
fun void breakDirtBlock() {
    // Set random filter parameters
    800 + Math.random2f(-100, 100) => filter.freq; // Randomize around 800 Hz
    4 + Math.random2f(-1, 1) => filter.Q;          // Randomize Q factor around 4

    // Trigger the envelope
    env.keyOn();
    0.05::second => now;
    env.keyOff();
}

// Play the sound once with random modulation
breakDirtBlock();
1::second => now; // Allow time for the sound to play out
