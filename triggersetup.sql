DROP TABLE IF EXISTS Manuscript;
DROP TABLE IF EXISTS Reviewer; 
DROP TABLE IF EXISTS Feedback;
DROP TABLE IF EXISTS Reviewer_ICode;


CREATE TABLE Manuscript (
id INT PRIMARY KEY AUTO_INCREMENT,
title VARCHAR(45) NOT NULL,
body BLOB NOT NULL,
received_date DATE NOT NULL,
man_status VARCHAR(45) NOT NULL DEFAULT('received'),
ICode_id MEDIUMINT NOT NULL REFERENCES Editor(id),
editor_id INT NOT NULL REFERENCES RICodes(code),
pages INT UNSIGNED NOT NULL,
status_last_updated DATE);

CREATE TABLE Reviewer (
id INT PRIMARY KEY AUTO_INCREMENT,
fname VARCHAR(45) NOT NULL,
lname VARCHAR(45) NOT NULL,
email VARCHAR(45) NOT NULL,
organization_id INT NOT NULL REFERENCES Organizations(id));

CREATE TABLE Reviewer_ICode (
reviewer_id INT NOT NULL REFERENCES Reviewer(id),
ICode_id MEDIUMINT NOT NULL REFERENCES RICodes(code),
PRIMARY KEY (reviewer_id, ICode_id));
  
CREATE TABLE Feedback (
manuscript_id INT NOT NULL REFERENCES Manuscript(id),
reviewer_id INT NOT NULL REFERENCES Reviewer(id) ON DELETE CASCADE,
A_score INT UNSIGNED,
C_score INT UNSIGNED,
M_score INT UNSIGNED,
E_score INT UNSIGNED,
recommendation VARCHAR(6),
recommendation_date DATE,
assigned_at TIMESTAMP NOT NULL DEFAULT NOW(),
PRIMARY KEY (manuscript_id, reviewer_id));

INSERT INTO Manuscript VALUES (1,"Nulla aliquet. Proin","lectus. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec dignissim magna a tortor. Nunc commodo auctor velit. Aliquam nisl. Nulla eu neque pellentesque massa lobortis ultrices. Vivamus rhoncus. Donec est. Nunc ullamcorper, velit in aliquet lobortis, nisi nibh lacinia orci, consectetuer euismod est arcu ac orci. Ut semper pretium neque. Morbi quis urna. Nunc quis arcu vel quam dignissim pharetra. Nam ac nulla. In tincidunt congue turpis. In condimentum. Donec at arcu. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae Donec tincidunt. Donec vitae erat vel pede blandit congue. In","2018-03-29","received",57,7,19,"2018-08-09");
INSERT INTO Manuscript VALUES (2,"viverra. Donec tempus,","ac mattis ornare, lectus ante dictum mi, ac mattis velit justo nec ante. Maecenas mi felis, adipiscing fringilla, porttitor vulputate, posuere vulputate, lacus. Cras interdum. Nunc sollicitudin commodo ipsum. Suspendisse non leo. Vivamus nibh dolor, nonummy ac, feugiat non, lobortis quis, pede. Suspendisse dui. Fusce diam nunc, ullamcorper eu, euismod ac, fermentum vel, mauris. Integer sem elit, pharetra ut, pharetra sed, hendrerit a, arcu. Sed et libero. Proin mi. Aliquam gravida mauris ut mi. Duis risus odio, auctor vitae, aliquet nec, imperdiet nec, leo. Morbi neque tellus, imperdiet non, vestibulum nec, euismod in, dolor. Fusce feugiat. Lorem ipsum dolor sit","2019-01-21","received",76,5,9,"2018-08-19");
INSERT INTO Manuscript VALUES (3,"nibh. Quisque nonummy","dictum. Phasellus in felis. Nulla tempor augue ac ipsum. Phasellus vitae mauris sit amet lorem semper auctor. Mauris vel turpis. Aliquam adipiscing lobortis risus. In mi pede, nonummy ut, molestie in, tempus eu, ligula. Aenean euismod mauris eu elit. Nulla facilisi. Sed neque. Sed eget lacus. Mauris non dui nec urna suscipit nonummy. Fusce fermentum fermentum arcu. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae Phasellus ornare. Fusce mollis. Duis sit amet diam eu dolor egestas rhoncus. Proin nisl sem, consequat nec, mollis vitae, posuere at, velit. Cras lorem lorem, luctus ut, pellentesque eget, dictum","2018-02-22","under review",32,9,13,"2018-07-19");
INSERT INTO Manuscript VALUES (4,"elit, a feugiat","penatibus et magnis dis parturient montes, nascetur ridiculus mus. Aenean eget magna. Suspendisse tristique neque venenatis lacus. Etiam bibendum fermentum metus. Aenean sed pede nec ante blandit viverra. Donec tempus, lorem fringilla ornare placerat, orci lacus vestibulum lorem, sit amet ultricies sem magna nec quam. Curabitur vel lectus. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec dignissim magna a tortor. Nunc commodo auctor velit. Aliquam nisl. Nulla eu neque pellentesque massa lobortis ultrices. Vivamus rhoncus. Donec est. Nunc ullamcorper, velit in aliquet lobortis, nisi nibh lacinia orci, consectetuer euismod est arcu ac orci. Ut semper","2018-08-03","under review",119,2,14,"2018-08-09");
INSERT INTO Manuscript VALUES (5,"parturient montes, nascetur","et netus et malesuada fames ac turpis egestas. Fusce aliquet magna a neque. Nullam ut nisi a odio semper cursus. Integer mollis. Integer tincidunt aliquam arcu. Aliquam ultrices iaculis odio. Nam interdum enim non nisi. Aenean eget metus. In nec orci. Donec nibh. Quisque nonummy ipsum non arcu. Vivamus sit amet risus. Donec egestas. Aliquam nec enim. Nunc ut erat. Sed nunc est, mollis non, cursus non, egestas a, dui. Cras pellentesque. Sed dictum. Proin eget odio. Aliquam vulputate ullamcorper magna. Sed eu eros. Nam consequat dolor vitae dolor. Donec fringilla. Donec feugiat metus sit amet ante. Vivamus non lorem","2018-08-16","under review",10,2,12,"2018-10-10");
INSERT INTO Manuscript VALUES (6,"dui. Cras pellentesque.","porttitor vulputate, posuere vulputate, lacus. Cras interdum. Nunc sollicitudin commodo ipsum. Suspendisse non leo. Vivamus nibh dolor, nonummy ac, feugiat non, lobortis quis, pede. Suspendisse dui. Fusce diam nunc, ullamcorper eu, euismod ac, fermentum vel, mauris. Integer sem elit, pharetra ut, pharetra sed, hendrerit a, arcu. Sed et libero. Proin mi. Aliquam gravida mauris ut mi. Duis risus odio, auctor vitae, aliquet nec, imperdiet nec, leo. Morbi neque tellus, imperdiet non, vestibulum nec, euismod in, dolor. Fusce feugiat. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aliquam auctor, velit eget laoreet posuere, enim nisl elementum purus, accumsan interdum libero dui","2019-07-13","under review",35,7,6,"2018-08-09");
INSERT INTO Manuscript VALUES (7,"nulla ante, iaculis","vestibulum lorem, sit amet ultricies sem magna nec quam. Curabitur vel lectus. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec dignissim magna a tortor. Nunc commodo auctor velit. Aliquam nisl. Nulla eu neque pellentesque massa lobortis ultrices. Vivamus rhoncus. Donec est. Nunc ullamcorper, velit in aliquet lobortis, nisi nibh lacinia orci, consectetuer euismod est arcu ac orci. Ut semper pretium neque. Morbi quis urna. Nunc quis arcu vel quam dignissim pharetra. Nam ac nulla. In tincidunt congue turpis. In condimentum. Donec at arcu. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia","2019-09-22","published",96,4,20,"2018-08-09");
INSERT INTO Manuscript VALUES (8,"nunc interdum feugiat.","montes, nascetur ridiculus mus. Aenean eget magna. Suspendisse tristique neque venenatis lacus. Etiam bibendum fermentum metus. Aenean sed pede nec ante blandit viverra. Donec tempus, lorem fringilla ornare placerat, orci lacus vestibulum lorem, sit amet ultricies sem magna nec quam. Curabitur vel lectus. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec dignissim magna a tortor. Nunc commodo auctor velit. Aliquam nisl. Nulla eu neque pellentesque massa lobortis ultrices. Vivamus rhoncus. Donec est. Nunc ullamcorper, velit in aliquet lobortis, nisi nibh lacinia orci, consectetuer euismod est arcu ac orci. Ut semper pretium neque. Morbi quis urna.","2019-04-08","typesetting",4,9,19,"2018-08-09");
INSERT INTO Manuscript VALUES (9,"rutrum. Fusce dolor","mattis ornare, lectus ante dictum mi, ac mattis velit justo nec ante. Maecenas mi felis, adipiscing fringilla, porttitor vulputate, posuere vulputate, lacus. Cras interdum. Nunc sollicitudin commodo ipsum. Suspendisse non leo. Vivamus nibh dolor, nonummy ac, feugiat non, lobortis quis, pede. Suspendisse dui. Fusce diam nunc, ullamcorper eu, euismod ac, fermentum vel, mauris. Integer sem elit, pharetra ut, pharetra sed, hendrerit a, arcu. Sed et libero. Proin mi. Aliquam gravida mauris ut mi. Duis risus odio, auctor vitae, aliquet nec, imperdiet nec, leo. Morbi neque tellus, imperdiet non, vestibulum nec, euismod in, dolor. Fusce feugiat. Lorem ipsum dolor sit amet,","2019-04-08","published",97,7,19,"2018-08-09");
INSERT INTO Manuscript VALUES (10,"neque non quam.","dapibus quam quis diam. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Fusce aliquet magna a neque. Nullam ut nisi a odio semper cursus. Integer mollis. Integer tincidunt aliquam arcu. Aliquam ultrices iaculis odio. Nam interdum enim non nisi. Aenean eget metus. In nec orci. Donec nibh. Quisque nonummy ipsum non arcu. Vivamus sit amet risus. Donec egestas. Aliquam nec enim. Nunc ut erat. Sed nunc est, mollis non, cursus non, egestas a, dui. Cras pellentesque. Sed dictum. Proin eget odio. Aliquam vulputate ullamcorper magna. Sed eu eros. Nam consequat dolor vitae dolor. Donec fringilla.","2018-07-27","published",122,1,19,"2018-08-09");

INSERT INTO Reviewer VALUES (1,"Tallulah","Rutledge","aliquet.diam@penatibuset.ca",2);
INSERT INTO Reviewer VALUES (2,"Cade","Stuart","sem.ut@semconsequatnec.ca",2);
INSERT INTO Reviewer VALUES (3,"Olivia","Winters","imperdiet@elementumpurusa.uk",8);
INSERT INTO Reviewer VALUES (4,"Brenna","Mathews","euismod@semperauctor.com",8);
INSERT INTO Reviewer VALUES (5,"Tamekah","Rosales","dignissim@lobortismauris.com",2);
INSERT INTO Reviewer VALUES (6,"Isabelle","Barrett","enim@auctorodioa.net",8);
INSERT INTO Reviewer VALUES (7,"Flynn","Ross","mollis.dui.in@molestieorci.org",5);
INSERT INTO Reviewer VALUES (8,"Bert","Stanley","elit.pellentesque@Etiam.net",1);
INSERT INTO Reviewer VALUES (9,"Juliet","Puckett","arcu.et.pede@ipsumprimisin.ca",8);
INSERT INTO Reviewer VALUES (10,"Brianna","Barrett","porttitor.tellus@necurna.org",4);

INSERT INTO Reviewer_ICode VALUES (1,57);
INSERT INTO Reviewer_ICode VALUES (1,76);
INSERT INTO Reviewer_ICode VALUES (1,32);
INSERT INTO Reviewer_ICode VALUES (2,119);
INSERT INTO Reviewer_ICode VALUES (2,10);
INSERT INTO Reviewer_ICode VALUES (3,119);
INSERT INTO Reviewer_ICode VALUES (3,10);
INSERT INTO Reviewer_ICode VALUES (3,96);
INSERT INTO Reviewer_ICode VALUES (4,119);
INSERT INTO Reviewer_ICode VALUES (5,10);
INSERT INTO Reviewer_ICode VALUES (5,96);
INSERT INTO Reviewer_ICode VALUES (6,96);
INSERT INTO Reviewer_ICode VALUES (6,4);
INSERT INTO Reviewer_ICode VALUES (6,97);
INSERT INTO Reviewer_ICode VALUES (7,4);
INSERT INTO Reviewer_ICode VALUES (7,97);
INSERT INTO Reviewer_ICode VALUES (8,97);
INSERT INTO Reviewer_ICode VALUES (8,122);
INSERT INTO Reviewer_ICode VALUES (8,35);
INSERT INTO Reviewer_ICode VALUES (9,122);
INSERT INTO Reviewer_ICode VALUES (9,43);
INSERT INTO Reviewer_ICode VALUES (9,35);
INSERT INTO Reviewer_ICode VALUES (10,122);
INSERT INTO Reviewer_ICode VALUES (10,35);
INSERT INTO Reviewer_ICode VALUES (10,4);

INSERT INTO Feedback VALUES (3,1,NULL,NULL,NULL,NULL,NULL,NULL,NOW());
INSERT INTO Feedback VALUES (4,2,NULL,NULL,NULL,NULL,NULL,NULL,NOW());
INSERT INTO Feedback VALUES (4,3,10,7,8,9,"accept","2018-08-17",NOW());
INSERT INTO Feedback VALUES (4,4,3,4,2,4,"reject","2018-08-16",NOW());
INSERT INTO Feedback VALUES (5,2,8,9,10,9,"accept","2018-09-18",NOW());
INSERT INTO Feedback VALUES (5,3,NULL,NULl,NULL,NULL,NULL,NULL,NOW());
INSERT INTO Feedback VALUES (5,5,NULL,NULL,NULL,NULL,NULL,NULL,NOW());
INSERT INTO Feedback VALUES (6,8,NULL,NULL,NULL,NULL,NULL,NULL,NOW());
INSERT INTO Feedback VALUES (7,9,NULL,NULL,NULL,NULL,NULL,NULL,NOW());
INSERT INTO Feedback VALUES (7,10,8,9,9,8,"accept","2018-09-18",NOW());
INSERT INTO Feedback VALUES (7,3,9,10,10,10,"accept","2018-09-09",NOW());
INSERT INTO Feedback VALUES (7,5,10,10,10,10,"accept","2018-09-09",NOW());
INSERT INTO Feedback VALUES (7,6,10,10,10,9,"accept","2018-09-09",NOW());
INSERT INTO Feedback VALUES (8,6,10,8,10,10,"accept","2018-09-09",NOW());
INSERT INTO Feedback VALUES (8,7,10,10,9,10,"accept","2018-09-09",NOW());
INSERT INTO Feedback VALUES (8,10,10,9,9,10,"accept","2018-09-09",NOW());
INSERT INTO Feedback VALUES (9,6,10,9,8,10,"accept","2018-09-09",NOW());
INSERT INTO Feedback VALUES (9,7,10,9,10,10,"accept","2018-09-09",NOW());
INSERT INTO Feedback VALUES (9,8,10,9,10,9,"accept","2018-09-09",NOW());
INSERT INTO Feedback VALUES (10,8,9,10,10,8,"accept","2018-09-09",NOW());
INSERT INTO Feedback VALUES (10,9,8,10,10,10,"accept","2018-09-09",NOW());
INSERT INTO Feedback VALUES (10,10,10,10,10,8,"accept","2018-09-09",NOW());