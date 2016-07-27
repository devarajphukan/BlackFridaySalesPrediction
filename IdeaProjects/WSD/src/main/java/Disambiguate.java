import opennlp.tools.chunker.ChunkerME;
import opennlp.tools.chunker.ChunkerModel;
import opennlp.tools.postag.POSModel;
import opennlp.tools.postag.POSTaggerME;
import org.deeplearning4j.models.embeddings.loader.WordVectorSerializer;
import org.deeplearning4j.models.word2vec.Word2Vec;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.LinkedHashMap;

public class Disambiguate {

    public static LinkedHashMap<String,String> getPosTags(String sentence){

        LinkedHashMap<String,String> posTagged = new LinkedHashMap<String,String>();
        InputStream modelIn = null;

        try {

            modelIn = new FileInputStream("/home/devaraj/IdeaProjects/TrendAnalysis/data/en-pos-maxent.bin");

            POSModel model = new POSModel(modelIn);
            POSTaggerME tagger = new POSTaggerME(model);

            String[] sentenceTokens = sentence.split(" ");
            String[] tags = tagger.tag(sentenceTokens);

            for (int i = 0; i < sentenceTokens.length; i++) {
                posTagged.put(sentenceTokens[i], tags[i]);
            }
        }

        catch (IOException e) {
            e.printStackTrace();
        }

        finally {
            if (modelIn != null) {
                try {
                    modelIn.close();
                }
                catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }

        return posTagged;
    }

    public static ArrayList<String> getChunks(String sentence) {

        InputStream modelIn = null;
        ChunkerModel model = null;

        ArrayList<String> nounChunks = new ArrayList<String>();
        try {
            modelIn = new FileInputStream("/home/devaraj/IdeaProjects/TrendAnalysis/data/en-chunker.bin");
            model = new ChunkerModel(modelIn);
            ChunkerME chunker = new ChunkerME(model);

            LinkedHashMap<String, String> posTagged = getPosTags(sentence);

            String[] sentenceTokens = new String[posTagged.keySet().size()];
            String[] posTokens = new String[posTagged.keySet().size()];

            // Insert values in sentenceTokens and posTokens from LinkedHashMap
            int c = 0;
            for (String s : posTagged.values()) {
                sentenceTokens[c] = s;
                c++;
            }
            int d = 0;
            for (String s : posTagged.keySet()) {
                sentenceTokens[d] = s;
                d++;
            }

            String chunkTag[] = chunker.chunk(sentenceTokens, posTokens);
            for (int i = 0; i < chunkTag.length; i++) {
                System.out.println(sentenceTokens[i] + " : " + chunkTag[i]);

                if (chunkTag[i].contains("NP")) {
                    nounChunks.add(sentenceTokens[i]);
                }
            }


        } catch (IOException e) {
            // Model loading failed, handle the error
            e.printStackTrace();
        } finally {

            if (modelIn != null) {
                try {
                    modelIn.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
        return nounChunks;
    }

    public static double getCosSimilarity(String s1, String s2) throws IOException{

        Word2Vec word2Vec = WordVectorSerializer.loadFullModel("/home/devaraj/IdeaProjects/WSD/model.txt");
        double cosSim = word2Vec.similarity(s1, s2);
        return cosSim;
    }

    public static void main(String[] args) {

        String test = "My name is Devaraj Phukan and I like to play football";
        ArrayList<String> ns = getChunks(test);

        for (String s : ns) {
            System.out.println(s);
        }
    }
}

