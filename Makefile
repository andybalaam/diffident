APP_NAME=diffident
VERSION=0.2
TMP_DIR=/tmp/$(APP_NAME)
DESTDIR=/usr

all:
	mkdir -p bin/lib/diffident/
	cp -r src/* bin/lib/diffident/
	find bin/lib/diffident/ \( -name "*.pyc" -or -name "*~" \) -delete

	mkdir -p bin/bin/
	cp install/diffident bin/bin/diffident
	perl -p -i -e "s@__DESTDIR__@${DESTDIR}@g" bin/bin/diffident

clean:
	rm -rf bin pkg

install:
	mkdir -p ${DESTDIR}/lib/diffident
	cp -r bin/lib/diffident/* ${DESTDIR}/lib/diffident/
	cp install/diffident ${DESTDIR}/bin/

pkg-src:
	mkdir -p pkg
	rm -f pkg/$(APP_NAME)-*.tar.bz2
	- rm -r $(TMP_DIR)
	mkdir $(TMP_DIR)
	git archive --format=tar --prefix=$(APP_NAME)-$(VERSION)/ master > pkg/$(APP_NAME)-$(VERSION).tar
	bzip2 pkg/$(APP_NAME)-$(VERSION).tar

pkg-deb: pkg-src
	- rm -r $(TMP_DIR)
	mkdir -p $(TMP_DIR)
	cp pkg/$(APP_NAME)-$(VERSION).tar.bz2 $(TMP_DIR)/
	tar --directory $(TMP_DIR)/ \
		-xjf $(TMP_DIR)/$(APP_NAME)-$(VERSION).tar.bz2
	cd $(TMP_DIR)/$(APP_NAME)-$(VERSION)/; \
		echo | dh_make --single --copyright gpl -e axis3x3@users.sf.net -f \
			../$(APP_NAME)-$(VERSION).tar.bz2
	cp install/deb/changelog install/deb/control \
		install/deb/copyright $(TMP_DIR)/$(APP_NAME)-$(VERSION)/debian/
	cd $(TMP_DIR)/$(APP_NAME)-$(VERSION)/; \
		rm debian/README.Debian debian/*.ex debian/*.EX; \
		./configure; \
		dpkg-buildpackage -rfakeroot; \
		mv ../*.deb $(PWD)/pkg/
	rm -r $(TMP_DIR);

