d = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1];
v = [2.6, 2, 1.6, 1.3, 1.1, 0.9, 0.8, 0.7, 0.6];
nfd = [0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95];
nfv = [2.35, 1.75, 1.45, 1.1, 0.95, 0.85, 0.75, 0.6];

p = polyfit(v, d, 4);

figure
hold on
plot(v, p(1).*v.^4 + p(2).*v.^3 + p(3).*v.^2 + p(4).*v + p(5), "LineWidth", 3)
plot(v, d, 'g.', "MarkerSize", 20)
plot(nfv, nfd, 'r.', "MarkerSize", 20)
title("IR Sensor Voltage to Distance Calibration Curve")
xlabel("voltage (V)")
ylabel("distance (m)")
legend("fit curve", "data for fitting", "data for error")