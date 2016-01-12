c
c	Electrical rectangular network
c     n lines, m rows
c
c line 1 at v0
c line n at v1
c
c						   v(i-1,j)
c							|
c    node (i,j)       h(i,j)--o--h(i,j-1)
c							|
c						    v(i,j)
c
c	F&L reduction scheme requires four types of transformations
c  s2: sum of two impedances (series) 
c  p2: sum of two impedances (parallele)
c  t3: triangle-star followed by a sum
c  t4: triangle-star followed by a star-triangle
c 	
c
c
c  case 1: m >=n  
c  Examples: n=7, m=10
c
c      m                    3  2  1
c      ----------------------------    1
c      |  |  |  |  |  |  |  |  |  |  
c      o--1--1--1--1--o--o--o--o--o    2
c      |  |  |  |  |  |  |  |  |  |  
c      o--o--2--2--2--2--o--o--o--o    3
c      |  |  |  |  |  |  |  |  |  |  
c      o--o--o--3--3--3--3--o--o--o    
c      |  |  |  |  |  |  |  |  |  |  
c      o--o--o--o--4--4--4--4--o--o    
c      |  |  |  |  |  |  |  |  |  |  
c      o--o--o--o--o--5--5--5--5--o    
c      |  |  |  |  |  |  |  |  |  |  
c      ----------------------------    n
c
c
c      s+ (n-2-k)*t4 + p  for  k=0 to n-2
c
c  case 2: m < n  
c  Examples: n=7, m=6
c
c      m        3  2  1
c      ----------------    1
c      |  |  |  |  |  |  
c      o--1--o--o--o--o    2
c      |  |  |  |  |  |  
c      o--1--2--o--o--o    3
c      |  |  |  |  |  |  
c      o--1--2--3--o--o    
c      |  |  |  |  |  |  
c      o--o--2--3--4--o    
c      |  |  |  |  |  |  
c      o--o--o--3--4--o    
c      |  |  |  |  |  |  
c      ----------------    n
c
c      (n-m) [s+ (m-2)*t4 + t3]   for k=1 to n-m
c
c      s+ (m-2-k)*t4 + p  for k=0 to m-2
c
      include 'comm.inc'
c
	real*8 tiny,tpi
	parameter(tiny=1.d-40)
	parameter(tpi=2.*3.14159265)
	integer size,i,j,kw,ipc
	integer t0,t1,tfin,tstart
	real*8 v0,v1
	real*8 wc,w0,w1,w2
	double complex adm,imp,zz(3)
	integer samples,maxsamp
	real*8 rimp,iimp
	real*8 rs
c
	real*8 vomega(ns)
	real*8 mrimp(ns),miimp(ns)
	integer msee,kwmax
c
      open (12,file='input.txt')
	read(12,*) size
	read(12,*) idum0
	read(12,*) v0,v1
	read(12,*) npc
	read(12,*) (pcv(i),i=1,npc)
	read(12,*) w0,w1,w2
	read(12,*) maxsamp
	read(12,*) rangen
	read(12,*) msee
	close(12)
c
	cv0=dcmplx(v0,0.d0)
	cv1=dcmplx(v1,0.d0)
c
      open (21,file='outp.txt')
      open (22,file='time.txt')
c
	do ipc=1,npc
	pc = pcv(ipc)
c
	idum=idum0
c
	ncmax= nint( (2*size*size)*pc)
c
	samples=0
	call timer(tstart)
c
100	samples=samples+1
	if (samples.gt.maxsamp) goto 200
c
	rs=samples
	rs=dsqrt(rs)
c
	m=size
	n=m+2
	n_2=size
c
	call init
c	kw=0
c
	if (msee.eq.0) goto 1001
	call timer(t0)
1001	continue
c
	wc=w0-w2
	kwmax=int((w1-w0)/w2)+1
	write(*,*) kwmax
c
	do kw=1,kwmax
		wc=wc+w2
c		kw=kw+1
		m=size
		n=m+2
		n_2=size

		omega=(10.0**wc)
		vomega(kw)=wc
c
		comega=1.0d9/omega
 	 zz(1)=  dcmplx(0.0d0,0.d0)
 	 zz(2)=  dcmplx(1000.0d0,0.0d0)
 	 zz(3)=  dcmplx(0.0d0 ,-comega)
c 	 zz(2)=  dcmplx(1.0d6,0.0d0)
c 	 zz(3)=  dcmplx(1.0d0 ,0.d0)
c
		do i=1,n
			do j=1,m
				h(i,j)=zz(zh(i,j)) 
				v(i,j)=zz(zv(i,j))
			enddo
		enddo

		t=0.0
 1		m_2=m-2
		n_m=n-m
		call redcol
		m=m-1
		if (m.gt.1) goto 1 
		imp=czero
		do i=1,n-1
			imp=imp+v(i,1)
		enddo
		adm= cone/imp
c 
		rimp=real(imp)
		iimp=imag(imp)
c
		mrimp(kw)=rimp
		miimp(kw)=iimp
      enddo
c 
	if (msee.eq.0) goto 100
        call timer(t1)
c
	write(22,*) 10.*(t1-t0),' ms for',kw,' omega values',samples
	if  (mod(samples,msee).eq.0) then
	  write(*,*) 10.*(t1-t0),' ms for',kw,' omega values',samples
	endif
c
	write(21,*) 
	write(21,'( A2,i10)') '# ',samples
	do i=1,kwmax+1
	   write(21,*) sngl(vomega(i)),sngl(mrimp(i)),sngl(miimp(i))
	   write(23,*) pc,sngl(mrimp(i)),sngl(miimp(i))
	enddo
	goto 100
c
200	continue
c
      write(*,*) 'case:',pc,samples,' done...'
	enddo
c
      close(21)
      close(22)
	call timer(tfin)
	write(*,*) 10.*(tfin-tstart)
c
      end
c
      subroutine redcol
      include 'comm.inc'
      integer k,p,k1,p1
      integer i,j

c
      k1=n_2
      if (n_m.gt.0) then
        do k=1,n_m
	    i=k
	    j=m
          call stwo(i,j)
          do p=1,m_2
	      i=k+p
	      j=m-p
            call four(i,j)
	    enddo
	    i=k+m_2+1
	    j=1
          call three(i,j)
	  enddo
	  k1=m_2
	endif
c
	do k=0,k1
c
	  i=k+n_m+1
	  j=m
        call stwo(i,j)
	  p1=k1-k
        do p=1,p1
	      i=k+n_m+1+p
	      j=m-p
            call four(i,j)
	  enddo
	  i=k+n_m+2+p1
	  j= m-p1-1
        call ptwo(i,j)
      enddo
	return
	end
c
c
      subroutine four(i,j)
      include 'comm.inc'
      integer i,j
	complex*16 edelta
c
      delta=cone/(e + h(i,j) + v(i-1,j))
      edelta=e*delta
      e=h(i,j)*v(i-1,j)*delta
      h(i,j)=h(i,j)*edelta
      v(i-1,j)=v(i-1,j)*edelta
c
      delta= e*(h(i,j-1) + v(i,j)) + h(i,j-1)*v(i,j)
      e=delta/e
      edelta=delta/v(i,j)
      v(i,j)=delta/h(i,j-1)
	h(i,j-1)=edelta
      return
      end
c
      subroutine three(i,j)
      include 'comm.inc'
      integer i,j
	complex*16 edelta
c
      delta=cone/(e+h(i,j)+v(i-1,j))
	edelta=e*delta
      e=h(i,j)*v(i-1,j)*delta
      h(i,j)=h(i,j)*edelta
      v(i-1,j)=v(i-1,j)*edelta
      v(i,j)=v(i,j)+e
      return
      end
C
      subroutine stwo(i,j)
      include 'comm.inc'
      integer i,j
      e=h(i,j-1)+v(i,j)
      return
      end
C
      subroutine ptwo(i,j)
      include 'comm.inc'
      integer i,j
c
      v(i-1,j)=(e*v(i-1,j))/(e+v(i-1,j))
      return
      end
c
