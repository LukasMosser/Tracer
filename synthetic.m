close all
clear all
clc

r=load('ricker2.txt');
% plot(r)

imp=zeros(2001,1);
i1=10; i2=1800;

imp(i1)=1;
imp(i2)=1;
for i=1:50
    if rand<=0.7
        imp=zeros(2001,1);
        i1=200; i2=1800;
        rn1=randi([0 80]);
        rn2=randi([-80 300]);
        i1=i1+rn1;
        i2=i2+rn2;
        imp(i1)=1;
        imp(i2)=1;
    end
[syn1,lag]=xcorr(r,imp);
h=plot(syn1,lag); xlim([-0.5 1])
ht=text(.8,.8,.8,num2str(i));
pause (1)
delete(h)
delete(ht);
end

h=plot(syn1,lag/2);xlim([-0.5 1]);
