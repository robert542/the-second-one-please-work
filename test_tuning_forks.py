from analyse_class import Sound

filename = "trimmed\c512_grp3_trimmed.wav"
t1_file = "trimmed\guitar_tr1_trimmed_ns.wav"
t2_file = "trimmed\guitar_tr2_trimmed_ns.wav"
t3_file = "trimmed\guitar_tr3_trimmed_ns.wav"

# csound = Sound(filename=filename)
# csound.plot_fourier()

s1 = Sound(t1_file)
s2 = Sound(t2_file)
s3 = Sound(t3_file)

s3.plot_base_freq_mult()
s1.plot_multi_overlay(s2,s3)

