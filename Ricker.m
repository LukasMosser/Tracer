time=0:1e-3:1;
u=0.5;
fp=20;
ricker=(1-2*pi^2*fp^2.*(time-u).^2).*exp(-pi^2*fp^2.*(time-u).^2);
plot(ricker)

