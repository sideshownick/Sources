!c
  	  implicit none
      integer np,ns
      parameter (np=4096)
      parameter (ns=128)
!c
	  integer,parameter :: qp=selected_real_kind(16)
	  integer,parameter :: dp=selected_real_kind(8)
	  integer,parameter :: sp=selected_real_kind(4)
	  complex (kind=qp) :: cone,czero
	  parameter (cone=(1._qp,0._qp),czero=(0._qp,0._qp))
!c
      complex (kind=qp) current,delta,e,h(np,np),v(np,np),u(np,np)
	  complex (kind=qp) cv1,cv0
	  complex (kind=qp) vu,vd,hr,hl
!c
	  real (kind=dp) t,pc,pcv(64),omega,comega
!c
      integer idum,idum0,m,n,m_2,n_2,n_m,ncmax
	  integer nch,ncv,rangen,npc,nproc
!c
	  integer*1 zh(np,np),zv(np,np)
!c
	  common current,delta,e,h,v,u
      common cv0,cv1
	  common vu,vd,hr,hl
!c
	  common t,pc,pcv,omega,comega
!c
	  common idum,idum0,m,n,m_2,n_2,n_m,ncmax
	  common nch,ncv,rangen,npc,nproc
!c	  
	  common zh,zv
!c 
